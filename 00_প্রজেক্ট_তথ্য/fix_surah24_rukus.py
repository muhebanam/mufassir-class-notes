import glob
import json
import re
import subprocess
import sys
from pathlib import Path

base_dir = Path(r"d:\আমার গবেষণা\জালালাইন")
audit_py = base_dir / "00_প্রজেক্ট_তথ্য" / "audit_ruku.py"
s_dir = base_dir / "২৪_সূরা_আন-নূর"

bn_digits = "০১২৩৪৫৬৭৮৯"

canonical_titles = [
    "০. ভূমিকা", "০. সারসংক্ষেপ", "১. মূল", "২. লুগাভী", "৩. ই'রাব",
    "৪. কিরাআত", "৫. তাফসীর", "৬. শানে নুযূল", "৭. মুখাতাব", "৭. মতভেদ",
    "৮. আহকাম", "৯. উলূমুল কুরআন", "১০. বালাগাত", "১১. সমকালীন", "১১. সংশয়",
    "১২. আন্তঃআয়াত", "১২. সংযোগ", "১৩. দারস", "১৩. দরস", "১৪. প্রামাণ্য", "১৪. সূত্র",
    "১৫. গবেষণাগত", "১৫. সীমাবদ্ধতা"
]

def is_canonical(line):
    return any(f"## {t}" in line for t in canonical_titles)

for r in range(1, 10):
    bn = bn_digits[r]
    fn = list(s_dir.glob(f"রুকু-০{bn}_*.md"))[0]
    lines = fn.read_text(encoding="utf-8").splitlines()
    new_lines = []
    for line in lines:
        if line.startswith("#") and not is_canonical(line):
            # Check if it has something like ## 3. or ### 4.
            m = re.match(r"^(#{2,6})\s+([০-৯0-9]+)\.\s*(.*)", line)
            if m:
                hashes, num, rest = m.groups()
                new_lines.append(f"### ({num}) {rest}")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    content = "\n".join(new_lines)
    if r == 4:
        content = re.sub(r"«([^»]*?مِنْ[”\"]?\s*زَائِدَةٌ[^»]*?)»", r"“\1”", content)
    fn.write_text(content, encoding="utf-8")

print("Auditing all 9 rukus of Surah 24:")
passed = 0
for r in range(1, 10):
    bn = bn_digits[r]
    fn = list(s_dir.glob(f"রুকু-০{bn}_*.md"))[0]
    res = subprocess.run([sys.executable, str(audit_py), str(fn)], capture_output=True, text=True, encoding="utf-8")
    if res.returncode == 0:
        print(f"Surah 24 Ruku {r}: PASSED")
        passed += 1
    else:
        print(f"Surah 24 Ruku {r}: FAILED")
        for line in res.stdout.splitlines():
            if "ERROR" in line or "FAILED" in line:
                print(f"   {line}")

print(f"=== Surah 24: {passed}/9 Passed ===")
