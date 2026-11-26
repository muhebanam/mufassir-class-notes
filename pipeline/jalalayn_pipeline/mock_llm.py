"""শুধু প্লাম্বিং-পরীক্ষার জন্য নকল LLM। আউটপুটে [MOCK-OUTPUT] চিহ্ন থাকে; merge/audit মক-আউটপুট আসল ফাইলে যেতে দেয় না।"""
from __future__ import annotations

import json
import re


def _ctx(user: str):
    m = re.search(r"```json\n(.*?)\n```", user, re.S)
    ctx = json.loads(m.group(1))
    srcs = {m.group(1): m.group(2) for m in re.finditer(r"\[SRC id=(\S+)[^\]]*\]\n(.*?)\n\[/SRC\]", user, re.S)}
    return ctx, srcs


def _quote(text: str, n=5, start=0) -> str:
    w = re.findall(r"[\u0600-\u06FF]+", text)
    if start >= len(w):
        start = 0
    return "«" + " ".join(w[start:start + n]) + "»"


def mock_fn(messages) -> str:
    user = messages[1]["content"]
    ctx, srcs = _ctx(user)
    sk = ctx["task"]["skill"]
    keys = ctx["task"]["block_keys"]
    ayat = {a["num"]: a for a in ctx["ayat"]}
    out = []
    M = "[MOCK-OUTPUT]"
    if sk == "ayah-translation-jalalayn":
        jid = next(s["id"] for s in ctx["sources"] if s["role"] == "jalalayn")
        for k in keys:
            a = ayat[int(k)]
            out.append(f"<!-- BLOCK:{k} -->\n<!-- PART:TRANSLATION_ROW_START -->\n| **{a['num_bn']}** | {{{{AYAH_TEXT}}}} | {M} শব্দানুগ | {M} সাবলীল |\n<!-- PART:TRANSLATION_ROW_END -->\n"
                       f"<!-- PART:JALALAYN_START -->\n- **আয়াত {a['num_bn']}:**\n\n  - **মূল আরবি ইবারত ({ctx['jalalayn_author']}):**\n    > {_quote(srcs[jid], 3, (int(k) - 1) * 3)} [src:{jid}]\n  - **বঙ্গানুবাদ ও টীকা:** {M} অনুবাদ।\n<!-- PART:JALALAYN_END -->")
    elif sk == "ayah-lughah-irab":
        for k in keys:
            a = ayat[int(k)]
            w = a["text_uthmani"].split()[0]
            out.append(f"<!-- BLOCK:{k} -->\n<!-- PART:MUFRADAT_ROWS_START -->\n| **{w}** | মূল | ওযন | {M} অর্থ | পরিভাষা | যাচাইসাপেক্ষ | যাচাইসাপেক্ষ | যাচাইসাপেক্ষ |\n<!-- PART:MUFRADAT_ROWS_END -->\n"
                       f"<!-- PART:IRAB_START -->\n### আয়াত {a['num_bn']}: ﴿{' '.join(a['text_uthmani'].split()[:3])}﴾\n\n- {M} ই'রাব ১ (আয়াত {a['num_bn']})।\n- {M} ই'রাব ২।\n- {M} জুমলা বিশ্লেষণ।\n<!-- PART:IRAB_END -->")
    elif sk == "ayah-qiraat-note":
        for k in keys:
            a = ayat[int(k)]
            qs = [r["qid"] for r in ctx["qiraat_rows"] if r["ayah"] == int(k)]
            out.append(f"<!-- BLOCK:{k} -->\n<!-- PART:QIRAAT_IMPACT_START -->\n### আয়াত {a['num_bn']} — কিরাআতের তাফসীর ও প্রভাব\n\n- {M} প্রথম পাঠ [{qs[0]}] অর্থে প্রভাব ফেলে।\n<!-- PART:QIRAAT_IMPACT_END -->")
    elif sk == "tafsir-hadith-unit":
        k = keys[0]
        first = ctx["task"]["ayat"][0]
        last = ctx["task"]["ayat"][-1]
        from_ = ayat[first]["num_bn"] + ("" if first == last else "–" + ayat[last]["num_bn"])
        sid_ = next(s["id"] for s in ctx["sources"] if s["role"] == "tafsir")
        out.append(f"<!-- BLOCK:{k} -->\n<!-- PART:COMPARATIVE_TAFSIR_START -->\n#### আয়াত {from_} — তুলনামূলক তাফসীর\n- {M} তাফসীর: {_quote(srcs[sid_])} [src:{sid_}]\n<!-- PART:COMPARATIVE_TAFSIR_END -->\n"
                   f"<!-- PART:SHANE_NUZUL_HADITH_START -->\nNONE\n<!-- PART:SHANE_NUZUL_HADITH_END -->")
    else:
        parts = ctx["task"]["parts"]
        body = {
            "SEC0_MAKASID": f"{M} রুকুর কেন্দ্রীয় উদ্দেশ্য সংক্ষেপে।\n\n### মূল আলোচ্য বিষয়\n- {M} বিষয় ১।",
            "SEC12_CONNECTIONS": f"প্রযোজ্য নয় — {M} এই রুকুতে আলাদা আন্তঃআয়াত সংযোগ নেই।",
            "SEC7_IKHTILAF": f"{M} মতভেদ নেই, এই অংশে কোনো প্রধান ইখতিলাফ নেই।",
            "SEC8_AHKAM": f"প্রযোজ্য নয় — {M} ফিকহী আহকাম নেই।",
        }
        out.append("<!-- BLOCK:RUKU -->")
        for p in parts:
            out.append(f"<!-- PART:{p}_START -->\n{body.get(p, M + ' ' + p + ' বিষয়বস্তু (মক)।')}\n<!-- PART:{p}_END -->")
    return "\n".join(out) + "\n"
