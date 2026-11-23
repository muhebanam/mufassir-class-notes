import os, sys, glob, re, json
from pathlib import Path

# Add project info dir for audit_ruku
sys.path.append(r'd:\আমার গবেষণা\জালালাইন\00_প্রজেক্ট_তথ্য')
from audit_ruku import audit_file, to_ascii_int

BENGALI_DIGITS = "০১২৩৪৫৬৭৮৯"
def to_bn(n: int) -> str:
    return "".join(BENGALI_DIGITS[int(c)] for c in str(n))

def to_bn_pad(n: int) -> str:
    return "".join(BENGALI_DIGITS[int(c)] for c in f"{n:02d}")

# Load ruku map
with open(r'd:\আমার গবেষণা\জালালাইন\00_প্রজেক্ট_তথ্য\ruku_map.json', 'r', encoding='utf-8') as f:
    ruku_map = json.load(f)['surahs']

print("Ready to implement Juz 21 upgrade...")
