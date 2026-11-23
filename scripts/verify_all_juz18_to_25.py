import sys
import subprocess
from pathlib import Path
import re

ROOT = Path(".")
audit_script = ROOT / "00_প্রজেক্ট_তথ্য" / "audit_ruku.py"

surah_folders = []
for p in sorted(ROOT.glob("*_সূরা_*")):
    if p.is_dir():
        m = re.match(r"^(\d+)_", p.name)
        if m:
            s_num = int(m.group(1))
            if 24 <= s_num <= 45:
                surah_folders.append((s_num, p))

print(f"Found {len(surah_folders)} Surahs in Juz 18 to 25 (Surahs 24 to 45).")

all_ruku_files = []
for s_num, p in surah_folders:
    files = sorted([f for f in p.glob("রুকু-*.md") if not f.name.endswith(".bak")])
    for f in files:
        all_ruku_files.append((s_num, f))

print(f"Total ruku files found: {len(all_ruku_files)}")

failed_audit = []
failed_trans = []
failed_muf = []
failed_irab = []
failed_sections = []

def to_bn(n):
    return ''.join(chr(ord(d) - ord('0') + 0x09E6) if '0' <= d <= '9' else d for d in str(n))

for s_num, fpath in all_ruku_files:
    text = fpath.read_text(encoding="utf-8")
    
    # 1. Translation placeholder
    if re.search(r"\(আয়াত \d+-এর প্রামাণ্য বঙ্গানুবাদ\)", text):
        failed_trans.append(fpath.name)
        
    # 2. Mufradat placeholder
    if "কুরআনিক শব্দরূপ ও আভিধানিক অর্থ" in text:
        failed_muf.append(fpath.name)
        
    # 3. Irab stub
    if "এই রুকুর আয়াতসমূহের মৌলিক বাক্যগঠন সুস্পষ্ট" in text:
        failed_irab.append(fpath.name)
        
    # 4. Canonical 16 sections
    for sec_num in range(16):
        bn_s = to_bn(sec_num)
        pat = rf"##\s+(?:{bn_s}|{sec_num})\."
        if not re.search(pat, text):
            failed_sections.append((fpath.name, sec_num))
            
    # 5. Run audit_ruku.py
    cmd = [sys.executable, str(audit_script), str(fpath)]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        failed_audit.append((fpath.name, res.stdout + res.stderr))

print("\n" + "="*50)
print("COMPREHENSIVE AUDIT REPORT: JUZ 18 TO JUZ 25")
print("="*50)
print(f"Total Rukus Evaluated: {len(all_ruku_files)}")
print(f"Audit Failures: {len(failed_audit)}")
print(f"Translation Placeholder Failures: {len(failed_trans)}")
print(f"Mufradat Placeholder Failures: {len(failed_muf)}")
print(f"I'rab Stub Failures: {len(failed_irab)}")
print(f"Section Structure Failures: {len(failed_sections)}")

if failed_audit:
    print("\nAudit Failures details:")
    for fn, err in failed_audit[:5]:
        print(f"  {fn}: {err[:200]}...")

if failed_trans:
    print(f"\nTranslation failures: {failed_trans}")
if failed_muf:
    print(f"\nMufradat failures: {failed_muf}")
if failed_irab:
    print(f"\nI'rab failures: {failed_irab}")
if failed_sections:
    print(f"\nSection failures: {failed_sections}")

if not any([failed_audit, failed_trans, failed_muf, failed_irab, failed_sections]):
    print("\n>>> ALL CHECKS PASSED WITH 100% SUCCESS! <<<")
else:
    print("\n>>> ISSUES DETECTED! <<<")
