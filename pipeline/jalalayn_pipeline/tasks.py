"""টাস্ক-পরিকল্পনা: কোন স্কিল কোন আয়াত/ইউনিট/রুকুতে চলবে; ব্যাচিং; অবস্থা সংরক্ষণ।"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

from .project import Project
from .sources import covers, load_sources, qiraat_rows_for
from .util import read_json, write_json

SKILLS = {
    "ayah-translation-jalalayn": dict(scope="ayat", level=1, parts=["TRANSLATION_ROW", "JALALAYN"]),
    "ayah-lughah-irab": dict(scope="ayat", level=1, parts=["MUFRADAT_ROWS", "IRAB"]),
    "ayah-qiraat-note": dict(scope="ayat", level=1, parts=["QIRAAT_IMPACT"]),
    "tafsir-hadith-unit": dict(scope="unit", level=1, parts=["COMPARATIVE_TAFSIR", "SHANE_NUZUL_HADITH"]),
    "ruku-makasid-connections": dict(scope="ruku", level=2, parts=["SEC0_MAKASID", "SEC12_CONNECTIONS"]),
    "ruku-ikhtilaf-ahkam": dict(scope="ruku", level=2, parts=["SEC7_IKHTILAF", "SEC8_AHKAM"]),
    "ruku-ulum-balaghat": dict(scope="ruku", level=2, parts=["SEC9_ULUM", "SEC10_BALAGHAT"]),
    "ruku-samakalin-dars": dict(scope="ruku", level=3, parts=["SEC11_SAMAKALIN", "SEC13_DARS"]),
    "ruku-limitations": dict(scope="ruku", level=3, parts=["SEC15_LIMITATIONS"]),
}


@dataclass
class Task:
    id: str
    skill: str
    scope: str
    level: int
    ayat: list
    parts: list
    keys: list                      # প্রত্যাশিত BLOCK কী
    status: str = "pending"         # pending|done|failed|blocked
    attempts: int = 0
    error: str = ""
    output: str = ""                # ওয়ার্ক-ডিরের আপেক্ষিক পাথ
    done_hash: str = ""
    provider: str = ""

    def to_dict(self):
        return asdict(self)


def ayat_tag(ayat: list[int]) -> str:
    if len(ayat) == 1:
        return f"{ayat[0]:03d}"
    if ayat == list(range(ayat[0], ayat[-1] + 1)):
        return f"{ayat[0]:03d}-{ayat[-1]:03d}"
    return "_".join(f"{a:03d}" for a in ayat)


def batch_ayat(proj: Project, sid: int, ayat: list[int], max_ayat: int, max_words: int) -> list[list[int]]:
    """পরপর ছোট আয়াত একসাথে (আউটপুট কিন্তু আয়াত-ভিত্তিক BLOCK); লম্বা আয়াত একা।"""
    batches, cur, words = [], [], 0
    for a in ayat:
        w = proj.quran.words(sid, a)
        if cur and (len(cur) >= max_ayat or words + w > max_words or a != cur[-1] + 1):
            batches.append(cur)
            cur, words = [], 0
        cur.append(a)
        words += w
    if cur:
        batches.append(cur)
    return batches


def tafsir_units(proj: Project, caps: dict, ayat: list[int], unit_max: int) -> list[list[int]]:
    """তাফসীর-গ্রন্থের (জালালাইন বাদে) ক্যাপচার যে আয়াত-গুচ্ছ একসাথে কভার করে, সেগুলো এক ইউনিট।"""
    parent = {a: a for a in ayat}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for c in caps.values():
        if c["kind"] != "turath_page" or proj.cfg.role_of(c["book_id"]) != "tafsir":
            continue
        cv = c.get("covers_ayat")
        if not isinstance(cv, list):
            continue
        cv = [a for a in cv if a in parent]
        for a in cv[1:]:
            parent[find(a)] = find(cv[0])
    groups: dict[int, list[int]] = {}
    for a in ayat:
        groups.setdefault(find(a), []).append(a)
    units = []
    for g in sorted(groups.values(), key=lambda g: g[0]):
        g = sorted(g)
        # অবিচ্ছিন্ন খণ্ডে ভাঙা + সর্বোচ্চ আকার
        chunk = []
        for a in g:
            if chunk and (a != chunk[-1] + 1 or len(chunk) >= unit_max):
                units.append(chunk)
                chunk = []
            chunk.append(a)
        if chunk:
            units.append(chunk)
    return sorted(units, key=lambda u: u[0])


def block_key_for_unit(u: list[int]) -> str:
    return str(u[0]) if len(u) == 1 else f"{u[0]}-{u[-1]}"


def plan(proj: Project, sid: int, rid: int) -> list[Task]:
    a0, a1 = proj.ruku_range(sid, rid)
    ayat = list(range(a0, a1 + 1))
    caps = load_sources(proj, sid, rid)
    r = proj.cfg.run
    existing = {t["id"]: t for t in (read_json(tasks_file(proj, sid, rid), {"tasks": []}).get("tasks", []))}
    out: list[Task] = []

    def mk(skill, ayat_list, keys, tid_suffix):
        spec = SKILLS[skill]
        t = Task(id=f"{skill}:{tid_suffix}", skill=skill, scope=spec["scope"], level=spec["level"],
                 ayat=ayat_list, parts=spec["parts"], keys=keys)
        old = existing.get(t.id)
        if old:
            for f in ("status", "attempts", "error", "output", "done_hash", "provider"):
                setattr(t, f, old.get(f, getattr(t, f)))
        out.append(t)

    for skill in ("ayah-translation-jalalayn", "ayah-lughah-irab"):
        for b in batch_ayat(proj, sid, ayat, r["batch_max_ayat"], r["batch_max_words"]):
            mk(skill, b, [str(a) for a in b], ayat_tag(b))
    q_ayat = sorted({row["ayah"] for row in qiraat_rows_for(caps)} & set(ayat))
    for b in batch_ayat(proj, sid, q_ayat, r["batch_max_ayat"], r["batch_max_words"]):
        mk("ayah-qiraat-note", b, [str(a) for a in b], ayat_tag(b))
    for u in tafsir_units(proj, caps, ayat, r["unit_max_ayat"]):
        mk("tafsir-hadith-unit", u, [block_key_for_unit(u)], ayat_tag(u))
    for skill in ("ruku-makasid-connections", "ruku-ikhtilaf-ahkam", "ruku-ulum-balaghat",
                  "ruku-samakalin-dars", "ruku-limitations"):
        mk(skill, ayat, ["RUKU"], "ruku")
    return out


def tasks_file(proj: Project, sid: int, rid: int):
    return proj.work_dir(sid, rid) / "tasks.json"


def save_tasks(proj: Project, sid: int, rid: int, tasks: list[Task]) -> None:
    write_json(tasks_file(proj, sid, rid), {"surah": sid, "ruku": rid, "tasks": [t.to_dict() for t in tasks]})


def load_tasks(proj: Project, sid: int, rid: int) -> list[Task]:
    d = read_json(tasks_file(proj, sid, rid))
    if not d:
        return []
    return [Task(**t) for t in d["tasks"]]


def safe_name(task_id: str) -> str:
    return task_id.replace(":", "__").replace(",", "_").replace("/", "_")
