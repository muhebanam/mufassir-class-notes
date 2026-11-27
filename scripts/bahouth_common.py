#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bahouth MCP কেন্দ্রীয় ক্লায়েন্ট ও হেল্পার (T1.0)
- JSON-RPC tools/call (SSE + JSON দুটোই হ্যান্ডেল)
- রিজিউমযোগ্য হারভেস্টের জন্য atomic write + failed.json
- key ফরম্যাট, root normalization, pagination হেল্পার
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import requests


BAHOUTH_URL = "https://bahouth.tafsir.net/mcp"
DEFAULT_LIMIT = 50
DEFAULT_SLEEP = 0.15
DEFAULT_TIMEOUT = 60
MAX_RETRIES = 3


class BahouthClient:
    """Streamable HTTP JSON-RPC ক্লায়েন্ট (SSE বা JSON রেসপন্স)"""

    def __init__(
        self,
        url: str = BAHOUTH_URL,
        sleep: float = DEFAULT_SLEEP,
        timeout: int = DEFAULT_TIMEOUT,
        retries: int = MAX_RETRIES,
    ):
        self.url = url
        self.sleep = sleep
        self.timeout = timeout
        self.retries = retries
        self._id = 0
        self.http = requests.Session()
        self.base_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }

    def _next_id(self) -> int:
        self._id += 1
        return self._id

    @staticmethod
    def _parse_body(resp: requests.Response) -> Any:
        ctype = resp.headers.get("Content-Type", "")
        text = resp.text
        if "text/event-stream" in ctype or text.lstrip().startswith(("event:", "data:")):
            messages = []
            for block in text.split("\n\n"):
                data_lines = [ln[5:].strip() for ln in block.splitlines() if ln.startswith("data:")]
                if data_lines:
                    try:
                        messages.append(json.loads("\n".join(data_lines)))
                    except json.JSONDecodeError:
                        pass
            return messages[-1] if messages else {"_unparsed_sse": text}
        try:
            return resp.json()
        except ValueError:
            return {"_unparsed": text}

    def call(
        self,
        method: str,
        params: Optional[Dict] = None,
        notify: bool = False,
    ) -> Any:
        payload = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            payload["params"] = params
        if not notify:
            payload["id"] = self._next_id()

        headers = dict(self.base_headers)

        last_err = None
        for attempt in range(1, self.retries + 1):
            try:
                resp = self.http.post(self.url, json=payload, headers=headers, timeout=self.timeout)
                if not notify:
                    resp.raise_for_status()
                time.sleep(self.sleep)
                return self._parse_body(resp)
            except Exception as e:
                last_err = e
                time.sleep(0.6 * attempt)
        return {"_error": f"{type(last_err).__name__}: {last_err}"}

    def list_verse_words(self, verse_key: str) -> Any:
        return self.call("tools/call", {"name": "list_verse_words", "arguments": {"verse_key": verse_key}})

    def list_root_verses(self, root_text: str, limit: int = DEFAULT_LIMIT, offset: int = 0) -> Any:
        return self.call("tools/call", {"name": "list_root_verses", "arguments": {"root_text": root_text, "limit": limit, "offset": offset}})

    def list_verse_topics(self, verse_key: str) -> Any:
        return self.call("tools/call", {"name": "list_verse_topics", "arguments": {"verse_key": verse_key}})

    def list_topic_verses(self, topic_id: int, limit: int = DEFAULT_LIMIT, offset: int = 0) -> Any:
        return self.call("tools/call", {"name": "list_topic_verses", "arguments": {"topic_id": topic_id, "limit": limit, "offset": offset}})

    def list_surah_verses(self, surah_id: int) -> Any:
        return self.call("tools/call", {"name": "list_surah_verses", "arguments": {"surah_id": surah_id}})

    def list_verse_qiraat(self, verse_key: str) -> Any:
        return self.call("tools/call", {"name": "list_verse_qiraat", "arguments": {"verse_key": verse_key}})

    def find_root(self, root_text: str) -> Any:
        return self.call("tools/call", {"name": "find_root", "arguments": {"root_text": root_text}})

    def get_verse(self, verse_key: str) -> Any:
        return self.call("tools/call", {"name": "get_verse", "arguments": {"verse_key": verse_key}})

    def list_verse_properties(self, verse_key: str) -> Any:
        return self.call("tools/call", {"name": "list_verse_properties", "arguments": {"verse_key": verse_key}})


def bahouth_key(surah: int, ayah: int) -> str:
    """Canonical verse_key: 'surah-ayah' (dash) — probe T0.2قرار।"""
    return f"{surah}-{ayah}"


def site_key_to_bahouth(key: str) -> str:
    """Site-internal key ('surah:ayah' বা 'surah-ayah') → bahouth dash format."""
    if ":" in key:
        s, a = key.split(":", 1)
        return f"{s}-{a}"
    return key


def bahouth_key_to_site(key: str) -> str:
    """Bahouth dash key → site colon format (e.g. for URL hashes)."""
    if "-" in key:
        s, a = key.split("-", 1)
        return f"{s}:{a}"
    return key


def strip_root_slashes(root_token_raw: str) -> str:
    """`/برك/` → `برك` (probe T0.2: bare root-only input to list_root_verses)."""
    if not root_token_raw:
        return ""
    r = root_token_raw.strip()
    if r.startswith("/") and r.endswith("/") and len(r) > 2:
        return r[1:-1]
    if r.startswith("/"):
        return r[1:]
    if r.endswith("/"):
        return r[:-1]
    return r


def normalize_arabic_for_matching(text: str) -> str:
    """
    Python equivalent of web/src/utils/wordByWordParser.js:normalizeArabicForMatching()
    Strips tashkeel, unifies hamza/alef/ta-marbuta/ya.
    """
    if not text:
        return ""
    return (
        text.replace("\u064b", "")  # fathatan
        .replace("\u064c", "")      # dammatan
        .replace("\u064d", "")      # kasratan
        .replace("\u064e", "")      # fatha
        .replace("\u064f", "")      # damma
        .replace("\u0650", "")      # kasra
        .replace("\u0651", "")      # shadda
        .replace("\u0652", "")      # sukun
        .replace("\u0670", "")      # dagger alif
        .replace("\u0640", "")      # tatweel
        .replace("\u0623", "\u0627")  # إ أ آ -> ا
        .replace("\u0625", "\u0627")
        .replace("\u0622", "\u0627")
        .replace("\u0671", "\u0627")
        .replace("\u0629", "\u0647")  # ة -> ه
        .replace("\u0649", "\u064a")  # ى -> ي
        .strip()
    )


def atomic_write_json(path: Union[str, Path], data: Any) -> None:
    """Temp file + os.replace for crash-safe writes."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, p)


def load_json_if_exists(path: Union[str, Path]) -> Optional[Any]:
    p = Path(path)
    if p.exists():
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return None


class HarvestState:
    """Resumable harvest state: collected items + failed calls log + retry support."""

    def __init__(self, surah: int, label: str, out_dir: Path):
        self.surah = surah
        self.label = label
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.data_file = self.out_dir / f"{label}_surah{surah}.json"
        self.failed_file = self.out_dir / f"{label}_surah{surah}_failed.json"
        self.collected: List[Any] = []
        self.failed: List[Dict] = []
        self._load()

    def _load(self):
        if self.data_file.exists():
            try:
                self.collected = json.loads(self.data_file.read_text(encoding="utf-8"))
            except Exception:
                self.collected = []
        if self.failed_file.exists():
            try:
                self.failed = json.loads(self.failed_file.read_text(encoding="utf-8"))
            except Exception:
                self.failed = []

    def add(self, item: Any):
        self.collected.append(item)
        atomic_write_json(self.data_file, self.collected)

    def add_failed(self, key: str, error: str, args: Dict):
        self.failed.append({"key": key, "error": error, "args": args, "ts": datetime.now(timezone.utc).isoformat()})
        atomic_write_json(self.failed_file, self.failed)

    def retry_failed(self, client: BahouthClient, func_name: str, sleep: float = DEFAULT_SLEEP) -> int:
        """Re-process failed entries; returns count retried."""
        if not self.failed:
            return 0
        remaining = []
        retried = 0
        for entry in self.failed:
            try:
                func = getattr(client, func_name)
                res = func(**entry["args"])
                payload = extract_payload(res)
                if payload:
                    self.add(payload)
                    retried += 1
                else:
                    remaining.append(entry)
            except Exception as e:
                remaining.append({**entry, "error": f"{type(e).__name__}: {e}"})
            time.sleep(sleep)
        self.failed = remaining
        atomic_write_json(self.failed_file, self.failed)
        return retried

    def stats(self) -> Dict:
        return {
            "surah": self.surah,
            "label": self.label,
            "collected": len(self.collected),
            "failed": len(self.failed),
            "data_file": str(self.data_file),
            "failed_file": str(self.failed_file),
        }


def extract_payload(resp: Any) -> Optional[Any]:
    """JSON-RPC রেসপন্স → structuredContent বা None (isError বা খালি হলে)।"""
    if not isinstance(resp, dict):
        return None
    if "_error" in resp:
        return None
    if "error" in resp:
        return None
    result = resp.get("result", resp)
    if isinstance(result, dict) and result.get("isError"):
        return None
    if isinstance(result, dict):
        sc = result.get("structuredContent")
        if sc is not None:
            return sc
        content = result.get("content")
        if isinstance(content, list):
            for c in content:
                if isinstance(c, dict) and c.get("type") == "text":
                    txt = c.get("text", "").strip()
                    if txt:
                        try:
                            return json.loads(txt)
                        except json.JSONDecodeError:
                            pass
    return result if result not in (None, "", [], {}) else None


def paginate_collect(
    client: BahouthClient,
    call_func,
    *args,
    limit: int = DEFAULT_LIMIT,
    max_items: Optional[int] = None,
    sleep: float = DEFAULT_SLEEP,
) -> Tuple[List[Any], Dict]:
    """
    Generic pagination collector for list_root_verses / list_topic_verses.
    Returns (collected_items, final_pagination_dict).
    Verifies len(collected) == pagination.total (truncation guard).
    """
    collected = []
    offset = 0
    total_expected = None
    has_more = True
    final_pag = {}

    while has_more:
        res = call_func(*args, limit=limit, offset=offset)
        payload = extract_payload(res)
        if not payload:
            break
        verses = payload.get("verses", [])
        pag = payload.get("pagination", {})
        final_pag = pag
        collected.extend(verses)
        if total_expected is None:
            total_expected = pag.get("total")
        has_more = pag.get("has_more", False)
        offset += limit
        if max_items and len(collected) >= max_items:
            break
        time.sleep(sleep)

    if total_expected is not None and len(collected) != total_expected:
        print(f"[WARN] Pagination truncation: collected={len(collected)} vs total={total_expected}", file=sys.stderr)

    return collected, final_pag


def make_schema_envelope(data: Any, schema_version: str = "1", server_url: str = BAHOUTH_URL) -> Dict:
    """Harvest output envelope with provenance."""
    return {
        "schema_version": schema_version,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "server_url": server_url,
        "data": data,
    }


def parse_args_with_retry_flag(args_list: List[str]) -> Tuple[List[str], bool]:
    """Common arg parsing: returns (clean_args, retry_failed_flag)."""
    retry = "--retry-failed" in args_list
    clean = [a for a in args_list if a != "--retry-failed"]
    return clean, retry


if __name__ == "__main__":
    print("bahouth_common.py - import only")