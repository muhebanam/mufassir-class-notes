"""প্রজেক্ট-পাথ ও লোডার: কনফিগ + Tanzil + রুকু-মানচিত্র।"""
from __future__ import annotations

from pathlib import Path

from .arabic import to_bn
from .config import Config
from .quran import Quran, SurahInfo, normalize_ruku_map
from .util import read_json


class Project:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self._quran = None
        self._map = None

    @property
    def quran(self) -> Quran:
        if self._quran is None:
            self._quran = Quran(self.cfg.info / self.cfg["tanzil_file"])
        return self._quran

    @property
    def ruku_map(self) -> dict[int, SurahInfo]:
        if self._map is None:
            raw = read_json(self.cfg.info / "ruku_map.json")
            if raw is None:
                raise FileNotFoundError(f"ruku_map.json পাওয়া যায়নি: {self.cfg.info}")
            self._map = normalize_ruku_map(raw)
        return self._map

    def surah(self, sid: int) -> SurahInfo:
        if sid not in self.ruku_map:
            raise KeyError(f"সূরা {sid} ruku_map.json-এ নেই — আগে মানচিত্রে যোগ করুন (jp validate-map)")
        return self.ruku_map[sid]

    def ruku_range(self, sid: int, rid: int) -> tuple[int, int]:
        s = self.surah(sid)
        if rid < 1 or rid > len(s.rukus):
            raise ValueError(f"সূরা {sid}-এ {len(s.rukus)}টি রুকু; অনুরোধ: {rid}")
        return s.rukus[rid - 1]

    def surah_dir(self, sid: int) -> Path:
        return self.cfg.base / self.surah(sid).dir_name

    def work_dir(self, sid: int, rid: int) -> Path:
        return self.cfg.work_root / f"s{sid:03d}" / f"r{rid:02d}"

    def sources_file(self, sid: int, rid: int) -> Path:
        return self.surah_dir(sid) / "_sources" / f"ruku_{rid:02d}_sources.json"

    def qiraat_table_file(self, sid: int, rid: int) -> Path:
        return self.surah_dir(sid) / "_sources" / f"ruku_{rid:02d}_qiraat_table.md"

    def ruku_md_path(self, sid: int, rid: int) -> Path:
        d = self.surah_dir(sid)
        a, b = self.ruku_range(sid, rid)
        bn2, en2 = to_bn(f"{rid:02d}"), f"{rid:02d}"
        for pat in (f"রুকু-{bn2}_*.md", f"রুকু-{en2}_*.md", f"রুকু-{rid}_*.md",
                    f"রুকু_{bn2}_*.md", f"রুকু_{en2}_*.md", f"রুকু_{rid}_*.md"):
            m = sorted(d.glob(pat)) if d.exists() else []
            if m:
                return m[0]
        return d / f"রুকু-{bn2}_আয়াত_{to_bn(a)}-{to_bn(b)}.md"

    def audit_key(self, sid: int, rid: int) -> str:
        return f"{sid}_{rid}"
