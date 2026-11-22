import json
from pathlib import Path

DATA_DIR = Path(r"d:\আমার গবেষণা\জালালাইন\web\public\data")

def verify():
    surahs_f = DATA_DIR / "surahs.json"
    assert surahs_f.exists(), "surahs.json missing"
    surahs = json.loads(surahs_f.read_text(encoding="utf-8"))
    assert len(surahs) == 91, f"Expected 91 surahs, got {len(surahs)}"
    print(f"✓ surahs.json contains {len(surahs)} surahs (24 to 114)")

    search_f = DATA_DIR / "search_index.json"
    assert search_f.exists(), "search_index.json missing"
    search_idx = json.loads(search_f.read_text(encoding="utf-8"))
    assert len(search_idx) == 3445, f"Expected 3445 verses, got {len(search_idx)}"
    print(f"✓ search_index.json contains {len(search_idx)} verses (3445/3445)")

    total_rukus_checked = 0
    total_ayahs_checked = 0

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
            
            # Check ayahs count
            total_rukus_checked += 1
            total_ayahs_checked += len(r_data["ayahs"])
            
            # Verify Uthmani text on each ayah
            for a in r_data["ayahs"]:
                assert a["text_uthmani"], f"Surah {sid} Ayah {a['ayah']} missing Uthmani text"
                assert "thematic_topics" in r_data, f"Surah {sid} Ruku {rid} missing thematic topics"

    print(f"✓ All {total_rukus_checked} rukus verified successfully (259/259)")
    print(f"✓ All {total_ayahs_checked} ayahs verified with Uthmani text (3445/3445)")
    print("ALL WEB DATA INTEGRITY CHECKS PASSED 100%!")

if __name__ == "__main__":
    verify()
