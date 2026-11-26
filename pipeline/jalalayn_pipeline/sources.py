"""উৎস-ক্যাপচার: ingest, sha256 সিল, যাচাই, প্রম্পটে রেন্ডার, কিরাআত-সারণি (স্ক্রিপ্ট-জেনারেটেড)।

নীতি: লেখক এজেন্ট কোনো MCP/ইন্টারনেট টুল পায় না; শুধু এখানে নিবন্ধিত ক্যাপচার পড়ে।
sha256 প্রমাণ করে ingest-এর পর টেক্সট বদলায়নি; মূল উৎসের খাঁটিত্ব নির্ভর করে আপনি আউটপুট হুবহু সেভ করেছেন কি না তার ওপর।
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .arabic import to_en
from .project import Project
from .util import canonical_hash, now_iso, read_json, sha256_text, write_json

KINDS = {
    "turath_page", "bahouth_qiraat", "bahouth_verses", "bahouth_root",
    "shamela_page", "tafsir_mcp", "hadith_mcp", "maher_hadith", "quran_mcp", "fiqh_fatwa", "bahouth_topics"
}
QIRAAT_HEADER = ["ক্র.", "আয়াত", "শব্দ (ক্রম)", "ক্বারী / রাবী (বাহাউথ)", "কিরাআতের পাঠভেদ ও নিয়ম (অবিকৃত মূল পাঠ)"]
QIRAAT_NA = ("প্রযোজ্য নয় — এই রুকুর আয়াতসমূহে দশ মুতাওয়াতির ক্বারীর মধ্যে "
             "বাহাউথ কিরাআত ডাটাবেজে কোনো পাঠভেদ নথিভুক্ত নেই।")


def payload_of(c: dict):
    k = c["kind"]
    if k == "bahouth_qiraat":
        return c.get("rows", [])
    if k == "bahouth_verses":
        return c.get("verses", [])
    if k == "bahouth_topics":
        return c.get("topics", [])
    if k == "hadith_mcp":
        return f"{c.get('text_ar', '')} {c.get('hadith_number', '')}"
    return c.get("text", "")


def seal(c: dict) -> dict:
    c["sha256"] = canonical_hash(payload_of(c))
    return c


def capture_text(c: dict) -> str:
    """প্রম্পট/যাচাইয়ের জন্য ক্যাপচারের টেক্সট রূপ।"""
    k = c["kind"]
    if k == "bahouth_qiraat":
        return "\n".join(f"{r.get('ayah')} | {r.get('word_cell')} | {r.get('readers')} | {r.get('rule')}" for r in c.get("rows", []))
    if k == "bahouth_verses":
        return "\n".join(f"{v.get('ayah')}: {v.get('text_raw')}" for v in c.get("verses", []))
    if k == "bahouth_topics":
        return "\n".join(f"- {t.get('title_raw', '')} (id: {t.get('topic_id')})" for t in c.get("topics", []))
    if k == "hadith_mcp":
        grades = c.get("grades") or ""
        return f"[{c.get('collection')}: {c.get('hadith_number')}] {c.get('text_ar')}\nঅধ্যায়: {c.get('chapter_title', '')}\nমান: {grades}"
    return c.get("text", "")


def load_sources(proj: Project, sid: int, rid: int) -> dict[str, dict]:
    d = read_json(proj.sources_file(sid, rid), {"captures": []})
    return {c["id"]: c for c in d.get("captures", [])}


def save_sources(proj: Project, sid: int, rid: int, caps: dict[str, dict]) -> None:
    write_json(proj.sources_file(sid, rid), {
        "schema": "jp-sources/1", "surah": sid, "ruku": rid, "updated_at": now_iso(),
        "captures": [caps[k] for k in sorted(caps)],
    })


def verify_hashes(caps: dict[str, dict]) -> list[str]:
    errs = []
    for cid, c in caps.items():
        if canonical_hash(payload_of(c)) != c.get("sha256"):
            errs.append(f"উৎস {cid}: sha256 মেলেনি — ingest-এর পর ফাইল বদলেছে")
    return errs


def covers(c: dict, ayat) -> bool:
    cv = c.get("covers_ayat")
    if cv == "surah":
        return True
    return bool(cv) and bool(set(cv) & set(ayat))


def roles(proj: Project, caps: dict[str, dict]) -> dict[str, str]:
    out = {}
    for cid, c in caps.items():
        k = c["kind"]
        if k == "turath_page":
            out[cid] = proj.cfg.role_of(c["book_id"])
        elif k in ("shamela_page", "tafsir_mcp", "quran_mcp"):
            out[cid] = c.get("role", "tafsir")
        elif k in ("hadith_mcp", "maher_hadith"):
            out[cid] = "hadith"
        elif k == "fiqh_fatwa":
            out[cid] = "fiqh"
        elif k == "bahouth_topics":
            out[cid] = "topics"
        else:
            out[cid] = k
    return out


def render_source(proj: Project, c: dict) -> str:
    meta = f"id={c['id']} | kind={c['kind']}"
    k = c["kind"]
    if k == "turath_page":
        b = proj.cfg.book(c["book_id"])
        meta += f" | book={c['book_id']} ({b.get('name_bn', '?')}) | page_id={c.get('page_id')}"
        if c.get("internal_page"):
            meta += f" | internal_page={c['internal_page']}"
    elif k == "shamela_page":
        meta += f" | book={c.get('book_title', '?')} | vol={c.get('volume', '?')} | page={c.get('page', '?')}"
        if c.get("url"):
            meta += f" | url={c.get('url')}"
    elif k == "hadith_mcp":
        meta += f" | collection={c.get('collection', '?')} | hadith={c.get('hadith_number', '?')}"
    elif k == "tafsir_mcp":
        meta += f" | source={c.get('source_name', '?')} | author={c.get('author', '?')}"
    elif k == "maher_hadith":
        meta += f" | title={c.get('title', '?')}"
    elif k == "fiqh_fatwa":
        meta += f" | source={c.get('source', '?')} | fatwa_id={c.get('fatwa_id', '?')}"

    cv = c.get("covers_ayat")
    meta += f" | covers={'surah' if cv == 'surah' else (','.join(map(str, cv)) if cv else '-')}"
    return f"[SRC {meta}]\n{capture_text(c)}\n[/SRC]"


# ---------- ingest ----------

def parse_qiraat_md(text: str) -> list[dict]:
    rows = []
    lines = [l.strip() for l in text.splitlines() if l.strip().startswith("|")]
    if len(lines) < 3:
        return rows
    hdr = [h.strip() for h in lines[0].strip("|").split("|")]

    def idx(sub):
        for i, h in enumerate(hdr):
            if sub in h:
                return i
        return None

    ia, iw, ir, iu = idx("আয়াত"), idx("শব্দ"), idx("ক্বারী"), idx("পাঠভেদ")
    if None in (ia, iw, ir, iu):
        return rows
    for ln in lines[2:]:
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if len(cells) <= max(ia, iw, ir, iu):
            continue
        m = re.search(r"\d+", to_en(cells[ia]))
        if not m:
            continue
        rows.append({"ayah": int(m.group()), "word_cell": cells[iw], "readers": cells[ir], "rule": cells[iu]})
    return rows


def rows_from_legacy_raw(raw: dict) -> list[dict]:
    """আগের _sources/ruku_XX_raw.json (schema 2.0-raw-mcp) থেকে — build_qiraat_table.py-র যুক্তির অনুরূপ।"""
    verses = {v["verse_key"]: v for v in raw.get("bahouth_verses", [])}
    qmap = raw.get("bahouth_qiraat", {})
    rows = []
    for key in sorted(verses, key=lambda k: int(k.split("-")[1])):
        v = verses[key]
        words = v["text_raw"].split()
        for ann in qmap.get(key, {}).get("annotations", []):
            order = ann.get("word_order_in_verse", 0)
            word = words[order - 1] if 1 <= order <= len(words) else f"[word#{order}]"
            raw_text = (ann.get("raw_text") or "").strip()
            if not raw_text:
                continue
            for seg in [s.strip() for s in raw_text.split("@") if s.strip()]:
                readers, rule = seg.split("/", 1) if "/" in seg else ("অনির্দিষ্ট", seg)
                rows.append({"ayah": v["ayah_number"], "word_cell": f"﴿{word}﴾ ({order})",
                             "readers": readers.strip(), "rule": rule.strip()})
    return rows


def _parse_txt_name(name: str):
    m = re.match(r"turath_(\d+)_(\d+)_a(surah|\d+(?:-\d+)?)\.txt$", name)
    if not m:
        return None
    book, page, cov = m.group(1), m.group(2), m.group(3)
    if cov == "surah":
        cv = "surah"
    elif "-" in cov:
        a, b = map(int, cov.split("-"))
        cv = list(range(a, b + 1))
    else:
        cv = [int(cov)]
    return int(book), int(page), cv


def ingest(proj: Project, sid: int, rid: int, inbox: Path) -> tuple[list[str], list[str]]:
    """inbox ফোল্ডারের ফাইল নিবন্ধন করে। (নিবন্ধিত আইডি, ত্রুটি/সতর্কতা) ফেরত।"""
    inbox = Path(inbox)
    caps = load_sources(proj, sid, rid)
    done, issues = [], []
    a0, a1 = proj.ruku_range(sid, rid)
    ruku_ayat = set(range(a0, a1 + 1))

    def add(c: dict, origin: Path):
        c["origin_file"] = origin.name
        c["file_sha256"] = sha256_text(origin.read_text(encoding="utf-8"))
        c.setdefault("captured_at", now_iso())
        seal(c)
        caps[c["id"]] = c
        done.append(c["id"])

    def check_turath(c: dict, origin: Path) -> bool:
        b = c.get("book_id")
        if proj.cfg.is_blocked_book(b):
            issues.append(f"{origin.name}: নিষিদ্ধ বই-আইডি {b}")
            return False
        if str(b) not in proj.cfg.books.get("allowed", {}):
            issues.append(f"{origin.name}: বই-আইডি {b} books.json-এর allowed তালিকায় নেই")
            return False
        if not str(c.get("text", "")).strip():
            issues.append(f"{origin.name}: টেক্সট ফাঁকা")
            return False
        cv = c.get("covers_ayat")
        if cv != "surah" and not (isinstance(cv, list) and cv and set(cv) <= ruku_ayat | set(cv)):
            issues.append(f"{origin.name}: covers_ayat অবৈধ")
            return False
        if isinstance(cv, list) and not (set(cv) & ruku_ayat):
            issues.append(f"{origin.name}: covers_ayat এই রুকুর আয়াত-সীমার বাইরে")
            return False
        return True

    for p in sorted(inbox.iterdir()):
        if not p.is_file():
            continue
        try:
            if p.suffix == ".json":
                d = json.loads(p.read_text(encoding="utf-8"))
                if "bahouth_verses" in d:  # legacy raw
                    rows = rows_from_legacy_raw(d)
                    add({"id": "bah-q", "kind": "bahouth_qiraat", "rows": rows, "tool": "legacy-raw"}, p)
                    verses = [{"ayah": v["ayah_number"], "text_raw": v["text_raw"]} for v in d["bahouth_verses"]]
                    add({"id": "bah-v", "kind": "bahouth_verses", "verses": verses, "tool": "legacy-raw"}, p)
                    if d.get("turath_pages"):
                        issues.append(f"{p.name}: legacy turath_pages ingest হয়নি (স্কিমা অজানা) — envelope JSON/txt আকারে দিন")
                    continue
                kind = d.get("kind")
                if kind not in KINDS:
                    issues.append(f"{p.name}: অজানা kind {kind!r}")
                    continue
                if kind == "turath_page":
                    c = {k: d.get(k) for k in ("book_id", "page_id", "internal_page", "covers_ayat", "text", "tool", "args", "captured_at")}
                    c.update(kind=kind, id=f"t{d.get('book_id')}-p{d.get('page_id')}")
                    if check_turath(c, p):
                        add(c, p)
                elif kind == "bahouth_qiraat":
                    rows = d.get("rows") or []
                    add({"id": "bah-q", "kind": kind, "rows": rows, "tool": d.get("tool")}, p)
                elif kind == "bahouth_verses":
                    add({"id": "bah-v", "kind": kind, "verses": d.get("verses") or [], "tool": d.get("tool")}, p)
                elif kind == "bahouth_root":
                    root = d.get("root")
                    if not root:
                        issues.append(f"{p.name}: root ফিল্ড নেই")
                        continue
                    text = d.get("text") or json.dumps(d.get("data", {}), ensure_ascii=False)
                    add({"id": f"bah-root-{root}", "kind": kind, "root": root, "text": text,
                         "covers_ayat": d.get("covers_ayat", "surah"), "tool": d.get("tool")}, p)
                elif kind == "shamela_page":
                    book_id = d.get("book_id", 0)
                    page = d.get("page", 0)
                    cid = f"sh{book_id}-p{page}"
                    c = {
                        "id": cid, "kind": kind, "book_id": book_id, "page": page,
                        "volume": d.get("volume"), "book_title": d.get("book_title", ""),
                        "author": d.get("author", ""), "url": d.get("url", ""),
                        "role": d.get("role", "tafsir"), "covers_ayat": d.get("covers_ayat", "surah"),
                        "text": d.get("text", "").strip(), "tool": d.get("tool", "shamela:get_page")
                    }
                    if not c["text"]:
                        issues.append(f"{p.name}: শামেলা টেক্সট ফাঁকা")
                        continue
                    add(c, p)
                elif kind == "tafsir_mcp":
                    subtype = d.get("subtype", "tafsir")
                    key = str(d.get("key", "1"))
                    cid = f"tm-{subtype}-{key}"
                    c = {
                        "id": cid, "kind": kind, "subtype": subtype, "key": key,
                        "source_name": d.get("source_name", ""), "author": d.get("author", ""),
                        "role": d.get("role", "tafsir"), "covers_ayat": d.get("covers_ayat", "surah"),
                        "text": d.get("text", "").strip(), "tool": d.get("tool", "tafsir-center")
                    }
                    if not c["text"]:
                        issues.append(f"{p.name}: tafsir_mcp টেক্সট ফাঁকা")
                        continue
                    add(c, p)
                elif kind == "hadith_mcp":
                    coll = d.get("collection", "hadith")
                    hnum = str(d.get("hadith_number", "1"))
                    cid = f"hm-{coll}-{hnum}"
                    c = {
                        "id": cid, "kind": kind, "collection": coll, "hadith_number": hnum,
                        "book_number": d.get("book_number"), "chapter_title": d.get("chapter_title", ""),
                        "text_ar": d.get("text_ar", "").strip(), "text_en": d.get("text_en", ""),
                        "grades": d.get("grades", ""), "cross_refs": d.get("cross_refs", []),
                        "covers_ayat": d.get("covers_ayat", "surah"), "tool": d.get("tool", "hadith-mcp")
                    }
                    if not c["text_ar"]:
                        issues.append(f"{p.name}: হাদীসের আরবি পাঠ ফাঁকা")
                        continue
                    add(c, p)
                elif kind == "maher_hadith":
                    doc_id = str(d.get("doc_id", "1"))
                    cid = f"mf-{doc_id}"
                    c = {
                        "id": cid, "kind": kind, "doc_id": doc_id, "title": d.get("title", ""),
                        "text": d.get("text", "").strip(), "covers_ayat": d.get("covers_ayat", "surah"),
                        "tool": d.get("tool", "maher-alfahel")
                    }
                    if not c["text"]:
                        issues.append(f"{p.name}: maher_hadith টেক্সট ফাঁকা")
                        continue
                    add(c, p)
                elif kind == "quran_mcp":
                    subtype = d.get("subtype", "gen")
                    key = str(d.get("key", "1"))
                    cid = f"qm-{subtype}-{key}"
                    c = {
                        "id": cid, "kind": kind, "subtype": subtype, "key": key,
                        "text": d.get("text", "").strip(), "role": d.get("role", "quran"),
                        "covers_ayat": d.get("covers_ayat", "surah"), "tool": d.get("tool", "quran-mcp")
                    }
                    if not c["text"]:
                        issues.append(f"{p.name}: quran_mcp টেক্সট ফাঁকা")
                        continue
                    add(c, p)
                elif kind == "fiqh_fatwa":
                    src = d.get("source", "fatwa")
                    fid = str(d.get("fatwa_id", "1"))
                    cid = f"fatwa-{src}-{fid}"
                    c = {
                        "id": cid, "kind": kind, "source": src, "fatwa_id": fid,
                        "question": d.get("question", ""), "answer": d.get("answer", ""),
                        "text": d.get("text", "").strip(), "covers_ayat": d.get("covers_ayat", "surah"),
                        "tool": d.get("tool", "islamqa")
                    }
                    if not c["text"]:
                        issues.append(f"{p.name}: ফতোয়া টেক্সট ফাঁকা")
                        continue
                    add(c, p)
                elif kind == "bahouth_topics":
                    tid = str(d.get("topic_id", "all"))
                    cid = f"bah-topic-{tid}"
                    topics = d.get("topics", [])
                    add({"id": cid, "kind": kind, "topic_id": tid, "topics": topics,
                         "covers_ayat": d.get("covers_ayat", "surah"), "tool": d.get("tool")}, p)
            elif p.suffix == ".md" and "qiraat" in p.name:
                rows = parse_qiraat_md(p.read_text(encoding="utf-8"))
                add({"id": "bah-q", "kind": "bahouth_qiraat", "rows": rows, "tool": "legacy-md"}, p)
            elif p.suffix == ".txt":
                parsed = _parse_txt_name(p.name)
                if not parsed:
                    issues.append(f"{p.name}: নামের বিন্যাস turath_<book>_<page>_a<from>-<to>.txt নয়")
                    continue
                book, page, cv = parsed
                c = {"id": f"t{book}-p{page}", "kind": "turath_page", "book_id": book, "page_id": page,
                     "covers_ayat": cv, "text": p.read_text(encoding="utf-8").strip(), "tool": "txt-inbox"}
                if check_turath(c, p):
                    add(c, p)
        except Exception as e:  # noqa: BLE001
            issues.append(f"{p.name}: পড়তে ব্যর্থ — {e}")
    save_sources(proj, sid, rid, caps)
    return done, issues


# ---------- কিরাআত সারণি ----------

def qiraat_rows_for(caps: dict[str, dict]) -> list[dict]:
    """সব bahouth_qiraat ক্যাপচার থেকে আইডিসহ (Q1, Q2…) সারি; আয়াত-ক্রমে।"""
    rows = []
    for c in caps.values():
        if c["kind"] == "bahouth_qiraat":
            rows.extend(c.get("rows", []))
    rows = sorted(enumerate(rows), key=lambda t: (t[1].get("ayah", 0), t[0]))
    out = []
    for n, (_, r) in enumerate(rows, 1):
        out.append({**r, "qid": f"Q{n}"})
    return out


def render_qiraat_table(rows: list[dict]) -> str:
    if not rows:
        return QIRAAT_NA
    head = "| " + " | ".join(QIRAAT_HEADER) + " |"
    sep = "| :---: | :---: | :--- | :--- | :--- |"
    body = [f"| {r['qid']} | **{r['ayah']}** | {r['word_cell']} | {r['readers']} | {r['rule']} |" for r in rows]
    return "\n".join([head, sep] + body)
