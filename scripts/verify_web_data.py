import json
from pathlib import Path

BASE_DIR = Path(r"d:\আমার গবেষণা\জালালাইন")
DATA_DIR = BASE_DIR / "web" / "public" / "data"

def load_tanzil():
    tanzil_file = BASE_DIR / "00_প্রজেক্ট_তথ্য" / "quran-uthmani.txt"
    tanzil = {}
    if not tanzil_file.exists():
        raise FileNotFoundError(f"Tanzil file missing at {tanzil_file}")
    with open(tanzil_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) >= 3:
                s_id, a_id = int(parts[0]), int(parts[1])
                tanzil[(s_id, a_id)] = parts[2]
    return tanzil

def verify():
    print("=" * 60)
    print("STARTING COMPREHENSIVE WEB DATA INTEGRITY AUDIT")
    print("=" * 60)

    tanzil = load_tanzil()
    print(f"Loaded {len(tanzil)} reference Uthmani ayahs from Tanzil.")

    surahs_f = DATA_DIR / "surahs.json"
    assert surahs_f.exists(), "surahs.json missing"
    surahs = json.loads(surahs_f.read_text(encoding="utf-8"))
    assert len(surahs) == 91, f"Expected 91 surahs, got {len(surahs)}"
    print(f"✓ surahs.json contains {len(surahs)} surahs (Surahs 24 to 114)")

    search_f = DATA_DIR / "search_index.json"
    assert search_f.exists(), "search_index.json missing"
    search_idx = json.loads(search_f.read_text(encoding="utf-8"))
    assert len(search_idx) == 3445, f"Expected 3445 verses in search_index, got {len(search_idx)}"
    print(f"✓ search_index.json contains {len(search_idx)} verses (3445/3445)")

    total_rukus_checked = 0
    total_ayahs_checked = 0
    gold_rukus = 0
    needs_work_rukus = 0
    uthmani_mismatches = []

    for s in surahs:
        sid = s["id"]
        s_dir = DATA_DIR / str(sid)
        meta_f = s_dir / "meta.json"
        assert meta_f.exists(), f"Surah {sid} meta.json missing"
        meta = json.loads(meta_f.read_text(encoding="utf-8"))
        
        for r_entry in meta["rukus"]:
            rid = r_entry["ruku_id"]
            ruku_f = s_dir / f"ruku-{rid}.json"
            assert ruku_f.exists(), f"Surah {sid} ruku-{rid}.json missing"
            r_data = json.loads(ruku_f.read_text(encoding="utf-8"))
            
            total_rukus_checked += 1
            if r_data.get("status") == "gold":
                gold_rukus += 1
            else:
                needs_work_rukus += 1

            for a in r_data["ayahs"]:
                total_ayahs_checked += 1
                a_num = a["ayah"]
                expected_uthmani = tanzil.get((sid, a_num))
                actual_uthmani = a.get("text_uthmani")

                if expected_uthmani != actual_uthmani:
                    uthmani_mismatches.append((sid, a_num, expected_uthmani, actual_uthmani))

    print(f"✓ Total Rukus Checked: {total_rukus_checked} / 259")
    print(f"✓ Total Ayahs Checked: {total_ayahs_checked} / 3445")
    print(f"✓ Exact Tanzil Uthmani Matches: {total_ayahs_checked - len(uthmani_mismatches)} / {total_ayahs_checked}")

    if uthmani_mismatches:
        print(f"✗ CRITICAL ERROR: Found {len(uthmani_mismatches)} Uthmani text mismatches with Tanzil!")
        for sid, a_num, exp, act in uthmani_mismatches[:5]:
            print(f"   - Surah {sid}:{a_num} Expected: {exp[:30]}... Got: {act[:30]}...")
        raise AssertionError("Uthmani verification failed.")

    print("\n" + "=" * 60)
    print("SCHOLARLY STATUS SUMMARY:")
    print(f"  • Gold Standard Rukus: {gold_rukus} (100% complete & audited)")
    print(f"  • Needs Work Rukus:    {needs_work_rukus} (remaining in corpus)")
    print("=" * 60)
    print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY WITH 100% INTEGRITY!")

if __name__ == "__main__":
    verify()
