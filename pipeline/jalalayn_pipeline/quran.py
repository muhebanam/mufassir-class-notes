"""Tanzil টেক্সট, রুকু-মানচিত্র (তিন স্কিমা স্বাভাবিকীকরণ) ও জালালাইন-রচয়িতা নীতি।"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .arabic import skeleton, strip_basmala, word_count


class Quran:
    def __init__(self, path: Path):
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Tanzil ফাইল পাওয়া যায়নি: {path}")
        self.v: dict[tuple[int, int], str] = {}
        self._count: dict[int, int] = defaultdict(int)
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("|", 2)
            if len(parts) < 3:
                continue
            s, a = int(parts[0]), int(parts[1])
            self.v[(s, a)] = strip_basmala(parts[2].strip(), s, a)
            self._count[s] = max(self._count[s], a)
        self._sk = {k: skeleton(t) for k, t in self.v.items()}
        self._joined = "|".join(self._sk.values())

    def verse(self, s: int, a: int) -> str:
        return self.v[(s, a)]

    def has(self, s: int, a: int) -> bool:
        return (s, a) in self.v

    def ayah_count(self, s: int) -> int:
        return self._count.get(s, 0)

    def verse_skeleton(self, s: int, a: int) -> str:
        return self._sk.get((s, a), "")

    def contains(self, sk: str) -> bool:
        """কঙ্কাল কি কুরআনের কোনো একক আয়াতের ভেতরে আছে?"""
        return bool(sk) and sk in self._joined

    def words(self, s: int, a: int) -> int:
        return word_count(self.verse(s, a))


def jalalayn_author(sid: int) -> dict:
    """ঐতিহাসিক নীতি: আল-কাহফ(১৮)–আন-নাস(১১৪) ও আল-ফাতিহা(১) মহাল্লীর; আল-বাকারা(২)–আল-ইসরা(১৭) সুয়ূতীর।"""
    if sid == 1 or sid >= 18:
        return {
            "key": "mahalli",
            "name_bn": "ইমাম জালালুদ্দীন আল-মহাল্লী (রহ.)",
            "must": ["মহাল্লী", "মাহাল্লী"],
            "must_not": ["সুয়ূতী", "সুয়ুতী", "সুয়ূত্বী", "সুয়ুত্বী", "সুয়ূতি"],
        }
    return {
        "key": "suyuti",
        "name_bn": "ইমাম জালালুদ্দীন আস-সুয়ূতী (রহ.)",
        "must": ["সুয়ূতী", "সুয়ুতী", "সুয়ূত্বী", "সুয়ুত্বী", "সুয়ূতি"],
        "must_not": ["মহাল্লী", "মাহাল্লী"],
    }


@dataclass
class SurahInfo:
    sid: int
    name_bn: str
    name_ar: str
    dir_name: str
    ayah_count: int
    rukus: list = field(default_factory=list)  # [(start, end), ...]


def normalize_ruku_map(raw: dict) -> dict[int, SurahInfo]:
    """তিন ধরনের এন্ট্রি সমর্থিত: [[s,e],...] / {ayah_start,ayah_end} / {ruku_number,ayah_start,ayah_end,...}."""
    out: dict[int, SurahInfo] = {}
    for k, v in raw.get("surahs", {}).items():
        sid = int(k)
        rukus = []
        for r in v.get("rukus", []):
            if isinstance(r, (list, tuple)):
                rukus.append((int(r[0]), int(r[1])))
            else:
                rukus.append((int(r["ayah_start"]), int(r["ayah_end"])))
        ac = v.get("ayah_count") or v.get("total_ayahs") or (rukus[-1][1] if rukus else 0)
        out[sid] = SurahInfo(
            sid=sid,
            name_bn=v.get("name_bn", ""),
            name_ar=v.get("name_ar", ""),
            dir_name=v.get("dir_name", ""),
            ayah_count=int(ac),
            rukus=rukus,
        )
    return out


def validate_map(quran: Quran | None, rmap: dict[int, SurahInfo]) -> tuple[list[str], list[str]]:
    """(ত্রুটি, তথ্য) ফেরত দেয়। ধারাবাহিকতা ও Tanzil-এর আয়াত-সংখ্যার সাথে মিল যাচাই করে।"""
    errors, info = [], []
    for sid in sorted(rmap):
        s = rmap[sid]
        if not s.dir_name:
            errors.append(f"সূরা {sid}: dir_name নেই")
        prev = 0
        for i, (a, b) in enumerate(s.rukus, 1):
            if a != prev + 1:
                errors.append(f"সূরা {sid} রুকু {i}: শুরু {a}, প্রত্যাশিত {prev + 1}")
            if b < a:
                errors.append(f"সূরা {sid} রুকু {i}: শেষ {b} < শুরু {a}")
            prev = b
        if prev != s.ayah_count:
            errors.append(f"সূরা {sid}: রুকুর শেষ আয়াত {prev} ≠ ayah_count {s.ayah_count}")
        if quran is not None and quran.ayah_count(sid) and quran.ayah_count(sid) != s.ayah_count:
            errors.append(f"সূরা {sid}: ayah_count {s.ayah_count} ≠ Tanzil {quran.ayah_count(sid)}")
    missing = [i for i in range(1, 115) if i not in rmap]
    if missing:
        info.append(f"মানচিত্রে নেই ({len(missing)}টি সূরা): {missing[0]}–{missing[-1]}" if len(missing) > 8 else f"মানচিত্রে নেই: {missing}")
    info.append(f"মানচিত্রে মোট {len(rmap)}টি সূরা, {sum(len(s.rukus) for s in rmap.values())}টি রুকু")
    return errors, info
