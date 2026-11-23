import glob, subprocess, sys

files = sorted(glob.glob("২৫_সূরা_আল-ফুরকান/রুকু*.md"))
print(f"Auditing {len(files)} files of Surah 25...")
all_pass = True
for f in files:
    res = subprocess.run([sys.executable, "00_প্রজেক্ট_তথ্য/audit_ruku.py", f], capture_output=True, text=True, encoding="utf-8")
    status = "PASSED" if "[PASSED]" in res.stdout else "FAILED"
    print(f"  {f.split('/')[-1]}: {status}")
    if status != "PASSED":
        all_pass = False
        print(res.stdout)

if all_pass:
    print("ALL RUKUS OF SURAH 25 PASSED 100%!")
