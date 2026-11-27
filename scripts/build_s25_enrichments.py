# -*- coding: utf-8 -*-
"""
সূরা আল-ফুরকান (২৫) — এনরিচমেন্ট ও raw আর্কাইভ বিল্ডার।
- হারভেস্টেড বিক্বাঈ (bikai_furqan_per_ayah.json) ও রাযী/ইবনে আশূর (transitions.txt) থেকে আরবি উদ্ধৃতি যোগ করে।
- লেখক-কৃত বাংলা (s25_munasabat_data*.py) থেকে prev/focus/next ও বিশ্লেষণ যোগ করে।
- আউটপুট: 2 raw JSON + 6 ruku enrichments + 6 MD-র অধ্যায় ৬/১২ পুনর্লিখন।
"""
import io, json, re, os, sys

ROOT = r"D:/আমার গবেষণা/জালালাইন"
WORK = os.path.join(ROOT, "_work", "s025")
SURAH_DIR = os.path.join(ROOT, "২৫_সূরা_আল-ফুরকান")
SRC = os.path.join(SURAH_DIR, "_sources")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from s25_munasabat_data import MUNASABAT_1
from s25_munasabat_data2 import MUNASABAT_2

MUN = {}
MUN.update(MUNASABAT_1)
MUN.update(MUNASABAT_2)
assert len(MUN) == 77, len(MUN)

def rd(p):
    return io.open(p, encoding="utf-8").read()

def trunc(s, n=420):
    s = (s or "").strip()
    return s if len(s) <= n else s[:n].rstrip() + "…"

# ---- load Bikai per-ayah ----
bikai = json.loads(rd(os.path.join(WORK, "bikai_furqan_per_ayah.json")))
BP = bikai["passages"]

# ---- load transitions (Razi + Ibn Ashur opening lines) ----
RZ, IA = {}, {}
cur = None
for line in rd(os.path.join(WORK, "transitions.txt")).splitlines():
    m = re.match(r"^\[(\d+)\]\s*RZ:\s*(.*)$", line)
    if m:
        cur = int(m.group(1)); RZ[cur] = m.group(2).strip(); continue
    m2 = re.match(r"^\s*IA:\s*(.*)$", line)
    if m2 and cur is not None:
        IA[cur] = m2.group(1).strip()

def bikai_citation(a):
    p = BP.get(str(a))
    if not p:
        return None
    return f"খণ্ড {p.get('vol','?')}, পৃ. {p.get('printed_page','?')} (shamela id=9098, পৃ. {p.get('shamela_page_id','?')})"

def build_nazm_scholars(a):
    d = MUN[a]
    out = []
    bp = BP.get(str(a))
    if bp and bp.get("excerpt"):
        out.append({
            "scholar": "ইমাম বুরহানুদ্দীন আল-বিক্বাঈ (ত. ৮৮৫ হি.)",
            "book": "নযমুদ দুরার ফী তানাসুবিল আয়াতি ওয়াস-সুওয়ার",
            "citation": bikai_citation(a),
            "arabic_excerpt": trunc(bp["excerpt"]),
            "analysis_bn": d["bikai"],
        })
    if RZ.get(a):
        out.append({
            "scholar": "ইমাম ফখরুদ্দীন আর-রাযী (ত. ৬০৬ হি.)",
            "book": "মাফাতীহুল গাইব (আত-তাফসীরুল কাবীর)",
            "citation": f"সূরা আল-ফুরকান, আয়াত {a}-এর তাফসীরের সূচনা (tafsir-center slug=razi)",
            "arabic_excerpt": trunc(RZ[a]),
            "analysis_bn": d["razi"],
        })
    if IA.get(a):
        out.append({
            "scholar": "ইমাম মুহাম্মাদ আত-তাহের ইবনে আশূর (ত. ১৩৯৩ হি.)",
            "book": "আত-তাহরীর ওয়াত-তানবীর",
            "citation": f"সূরা আল-ফুরকান, আয়াত {a} (tafsir-center slug=ibn_ashur)",
            "arabic_excerpt": trunc(IA[a]),
            "analysis_bn": d["ashur"],
        })
    return out

# ---- build nazm raw + enrichments ----
nazm_raw = {"surah_id": 25,
            "generated_by": "turath (biqai 9098) + tafsir-center (razi, ibn_ashur)",
            "biqai_nazm_durar_9098": {"book_id": 9098,
                "title": "نظم الدرر في تناسب الآيات والسور — البقاعي",
                "surah_section": "سورة الفرقان",
                "surah_intro_printed_ref": bikai.get("surah_intro", {}).get("printed_ref"),
                "ayahs": {}},
            "nazm_by_ayah": {}}

for a in range(1, 78):
    bp = BP.get(str(a), {})
    nazm_raw["biqai_nazm_durar_9098"]["ayahs"][str(a)] = {
        "shamela_page_id": bp.get("shamela_page_id"),
        "printed_ref": (f"ج{bp.get('vol','?')} ص{bp.get('printed_page','?')}" if bp else None),
        "arabic_excerpt": trunc(bp.get("excerpt", ""), 600) if bp else "",
    }
    nazm_raw["nazm_by_ayah"][str(a)] = {
        "biqai": trunc(bp.get("excerpt", ""), 600) if bp else "",
        "razi": trunc(RZ.get(a, ""), 600),
        "ibn_ashur": trunc(IA.get(a, ""), 600),
    }

io.open(os.path.join(SRC, "surah25_nazm_raw.json"), "w", encoding="utf-8").write(
    json.dumps(nazm_raw, ensure_ascii=False, indent=1))

# asbab nuzul raw (direct nuzul ayat with reports from MCP)
DIRECT = {27, 32, 68, 70}
SIRAH = {4, 5, 7, 8, 9}
asbab_raw = {"surah_id": 25,
             "generated_by": "tafsir-center (nuzool: wahidi + lubab al-nuql) + mathur",
             "policy": "স্বতন্ত্র শানে নুযূল কেবল যাচাইকৃত আয়াতে; বাকিতে has_direct_nuzul=false",
             "ayahs": {}}
for a in range(1, 78):
    has = a in DIRECT
    entry = {"ayah": a, "has_direct_nuzul": has,
             "sirah_context_only": (a in SIRAH), "nuzul_reports": [], "related_hadiths": []}
    if has:
        try:
            nj = json.loads(rd(os.path.join(WORK, "mcp", f"ayah_{a:02d}.json")))
            for src in nj.get("nuzool", {}).get("sources", []):
                entry["nuzul_reports"].append({
                    "source": src.get("attribution"),
                    "arabic_text": trunc(src.get("text_raw", ""), 1200),
                    "editorial_note": " ; ".join(fn.get("text", "") for fn in src.get("footnotes", [])),
                })
        except Exception:
            pass
    asbab_raw["ayahs"][str(a)] = entry
io.open(os.path.join(SRC, "surah25_asbab_nuzul_raw.json"), "w", encoding="utf-8").write(
    json.dumps(asbab_raw, ensure_ascii=False, indent=1))

# ---- enrichments per ruku ----
RUKU = {1: (1, 9), 2: (10, 20), 3: (21, 34), 4: (35, 44), 5: (45, 60), 6: (61, 77)}
SOURCE = "নযমুদ দুরার (আল-বিক্বাঈ), মাফাতিহুল গাইব (ইমাম রাযী) ও আত-তাহরীর ওয়াত-তানবীর (ইবনে আশূর)"
for rid, (s, e) in RUKU.items():
    ayahs = []
    for a in range(s, e + 1):
        d = MUN[a]
        ayahs.append({"ayah": a, "munasabat": {
            "prev_ayah_link": d["prev"],
            "current_ayah_focus": d["focus"],
            "next_ayah_link": d["next"],
            "source": SOURCE,
            "nazm_scholars": build_nazm_scholars(a),
        }})
    obj = {"surah_id": 25, "ruku_id": rid,
           "source_verification": "turath (biqai 9098), tafsir-center (razi, ibn_ashur)",
           "ayahs": ayahs}
    io.open(os.path.join(SRC, f"ruku_{rid:02d}_enrichments.json"), "w", encoding="utf-8").write(
        json.dumps(obj, ensure_ascii=False, indent=1))

print("raw + enrichments written; nazm_scholars sample ayah1:", len(build_nazm_scholars(1)))
print("RUKU files:", [f for f in os.listdir(SRC) if f.endswith("enrichments.json")])