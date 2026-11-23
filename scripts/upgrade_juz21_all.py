import re, os, sys, glob, json
from pathlib import Path

# Add project info dir
sys.path.append(r'd:\আমার গবেষণা\জালালাইন\00_প্রজেক্ট_তথ্য')
from audit_ruku import audit_file, to_ascii_int

BENGALI_DIGITS = "০১২৩৪৫৬৭৮৯"
def to_bn(n: int) -> str:
    return "".join(BENGALI_DIGITS[int(c)] for c in str(n))

def to_bn_pad(n: int) -> str:
    return "".join(BENGALI_DIGITS[int(c)] for c in f"{n:02d}")

def update_ruku_file(fpath: Path, translations: dict, mufradat_table: str, irab_text: str = None):
    content = fpath.read_text(encoding='utf-8')
    
    # 1. Update translations in Section 1
    for a_num, t_text in translations.items():
        bn_num = to_bn(a_num)
        old_pat = rf'\|\s*\*\*{bn_num}\*\*\s*\|\s*(﴿[^﴾]+﴾)\s*\|\s*\(আয়াত {bn_num}-এর প্রামাণ্য বঙ্গানুবাদ\)\s*\|'
        new_sub = rf'| **{bn_num}** | \1 | {t_text} |'
        content = re.sub(old_pat, new_sub, content)
        
    # 2. Update Mufradat table in Section 2
    sec2_pat = r'(## ২\. লুগাভী ও সরফী তাহকীক এবং মুফরাদাতুল কুরআন\s*\n\s*)(\|[\s\S]*?)(?=\n\n---\n\n## ৩\.)'
    m2 = re.search(sec2_pat, content)
    if m2:
        content = content[:m2.start(2)] + mufradat_table.strip() + content[m2.end(2):]
    else:
        # Fallback regex if spacing differs
        sec2_alt = r'## ২\. লুগাভী ও সরফী তাহকীক এবং মুফরাদাতুল কুরআন[\s\S]*?(?=---\s*\n\s*## ৩\.)'
        content = re.sub(sec2_alt, f"## ২. লুগাভী ও সরফী তাহকীক এবং মুফরাদাতুল কুরআন\n\n{mufradat_table.strip()}\n\n", content)

    # 3. Update I'rab in Section 3 if provided and currently a stub
    if irab_text and 'প্রযোজ্য নয় — এই রুকুর আয়াতসমূহের মৌলিক বাক্যগঠন সুস্পষ্ট' in content:
        sec3_pat = r'## ৩\. ই\'রাব ও নাহবী বিশ্লেষণ\s*\n\s*প্রযোজ্য নয় — এই রুকুর আয়াতসমূহের মৌলিক বাক্যগঠন সুস্পষ্ট; কোনো মতভেদপূর্ণ বা অস্পষ্ট নাহবী জটিলতা নেই\.'
        content = re.sub(sec3_pat, f"## ৩. ই'রাব ও নাহবী বিশ্লেষণ\n\n{irab_text.strip()}", content)
        
    fpath.write_text(content, encoding='utf-8')
    ok, errs, warns = audit_file(fpath, json_report=True)
    if not ok:
        print(f"Audit FAILED on {fpath.name}: {errs}")
    else:
        print(f"Audit PASSED on {fpath.name}")
    return ok

print("Helper functions defined.")
