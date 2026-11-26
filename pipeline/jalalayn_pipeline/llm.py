"""LLM প্রোভাইডার: litellm (প্রোডাকশন) ও callable/mock (টেস্ট)। রেট-লিমিট ও পুনঃচেষ্টাসহ।"""
from __future__ import annotations

import threading
import time


class RateLimiter:
    def __init__(self, rpm: int):
        self.interval = 60.0 / max(1, rpm)
        self.lock = threading.Lock()
        self.next = 0.0

    def wait(self):
        with self.lock:
            now = time.monotonic()
            delay = max(0.0, self.next - now)
            self.next = max(now, self.next) + self.interval
        if delay:
            time.sleep(delay)


class LiteLLMProvider:
    name = "litellm"

    def __init__(self, cfg):
        c = cfg.llm
        if not c.get("model"):
            raise SystemExit("মডেল নির্ধারিত নেই: config.json-এ llm.model দিন বা JP_MODEL পরিবেশ-চলক সেট করুন "
                             "(litellm মডেল-স্ট্রিং, যেমন আপনার প্রোভাইডারের নির্দেশিকা অনুযায়ী)।")
        self.c = c
        self.limiter = RateLimiter(cfg.run["rpm"])

    def complete(self, messages: list) -> str:
        try:
            import litellm  # noqa: WPS433
        except ImportError as e:  # pragma: no cover
            raise SystemExit("litellm ইনস্টল নেই: pip install -r pipeline/requirements.txt") from e
        last = None
        for n in range(int(self.c["api_retries"]) + 1):
            self.limiter.wait()
            try:
                r = litellm.completion(model=self.c["model"], messages=messages,
                                       temperature=self.c["temperature"], max_tokens=self.c["max_tokens"],
                                       timeout=self.c["timeout"])
                return r.choices[0].message.content or ""
            except Exception as e:  # noqa: BLE001 — রেট-লিমিট/নেটওয়ার্ক: ব্যাকঅফ
                last = e
                time.sleep(float(self.c["backoff_base"]) * (2 ** n))
        raise RuntimeError(f"API ব্যর্থ: {last}")


class CallableProvider:
    def __init__(self, fn, name="callable"):
        self.fn = fn
        self.name = name
        self.calls = 0
        self.lock = threading.Lock()

    def complete(self, messages: list) -> str:
        with self.lock:
            self.calls += 1
        return self.fn(messages)


def get_provider(cfg, name=None, fn=None):
    name = name or cfg.llm["provider"]
    if fn is not None:
        return CallableProvider(fn, name)
    if name == "mock":
        from .mock_llm import mock_fn
        return CallableProvider(mock_fn, "mock")
    if name == "litellm":
        return LiteLLMProvider(cfg)
    raise SystemExit(f"অজানা provider: {name}")
