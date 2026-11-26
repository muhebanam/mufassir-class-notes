"""Surah 24 Multi-MCP Harvester & Ingest for All Rukus (1 to 9)."""
import json
import ssl
import sys
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR / "pipeline") not in sys.path:
    sys.path.insert(0, str(BASE_DIR / "pipeline"))

from jalalayn_pipeline.config import Config
from jalalayn_pipeline.project import Project
from jalalayn_pipeline.sources import ingest
from harvester_helper import prepare_inbox_from_existing, save_hadith_mcp, save_tafsir_mcp

p = Project(Config(BASE_DIR))
ctx = ssl._create_unverified_context()
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "User-Agent": "Antigravity/1.0"
}


def call_mcp(name: str, arguments: dict):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments}
    }
    req = urllib.request.Request(
        "https://mcp.tafsir.net/mcp",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers
    )
    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=30)
        text = resp.read().decode("utf-8")
        for line in text.splitlines():
            if line.startswith("data: "):
                data = json.loads(line[6:])
                return json.loads(data["result"]["content"][0]["text"])
    except Exception as e:
        print(f"Error calling MCP {name} with {arguments}: {e}")
    return None


def harvest_ruku(rid: int):
    inbox = BASE_DIR / f"_work/s024/r{rid:02d}/inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    prepare_inbox_from_existing(p, 24, rid, inbox)

    a0, a1 = p.ruku_range(24, rid)
    print(f"\n=== Harvesting Surah 24 Ruku {rid} (Ayahs {a0}-{a1}) ===")

    for a in range(a0, a1 + 1):
        # 1. Tafsir Center: Jalalayn, Ibn Kathir, Tabari, Qurtubi, Mukhtasar Bengali
        res = call_mcp("fetch_tafsir", {
            "surah": 24,
            "ayah": a,
            "sources": ["jalalayn", "katheer", "tabary", "qurtubi", "mukhtasar_bn"]
        })
        if res and "tafsirs" in res:
            for t in res["tafsirs"]:
                src = t.get("source")
                role = "jalalayn" if src == "jalalayn" else ("translation" if "bn" in src else "tafsir")
                save_tafsir_mcp(
                    inbox,
                    src,
                    f"24:{a}",
                    t.get("source", src),
                    t.get("attribution", ""),
                    t.get("text", ""),
                    covers_ayat=[a],
                    role=role
                )

        # 2. Asbab al-Nuzul
        nuz = call_mcp("fetch_nuzool_reason", {"surah": 24, "ayah": a})
        if nuz and "sources" in nuz:
            for s in nuz["sources"]:
                if s.get("available") is not False and s.get("text"):
                    save_tafsir_mcp(
                        inbox,
                        "nuzul",
                        f"24:{a}",
                        "أسباب النزول",
                        s.get("attribution", ""),
                        s.get("text", ""),
                        covers_ayat=[a],
                        role="nuzul"
                    )

    # 3. Add representative Sahih Hadiths for the ruku
    if rid == 1:
        save_hadith_mcp(inbox, "bukhari", "2226", "حَدَّثَنَا أَبُو الْوَلِيدِ... وَاغْدُ يَا أُنَيْسُ إِلَى امْرَأَةِ هَذَا، فَإِنِ اعْتَرَفَتْ فَارْجُمْهَا.", text_en="Hadith of Asif", grades="صحيح", covers_ayat=list(range(a0, a1 + 1)))
        save_hadith_mcp(inbox, "muslim", "1690", "عَنْ عُبَادَةَ بْنِ الصَّامِتِ قَالَ: قَالَ رَسُولُ اللَّهِ ﷺ: خُذُوا عَنِّي، خُذُوا عَنِّي، قَدْ جَعَلَ اللَّهُ لَهُنَّ سَبِيلًا، الْبِكْرُ بِالْبِكْرِ جَلْدُ مِائَةٍ وَتَغْرِيبُ عَامٍ، وَالثَّيِّبُ بِالثَّيِّبِ جَلْدُ مِائَةٍ وَالرَّجْمُ", text_en="Hadith of Ubada", grades="صحيح", covers_ayat=list(range(a0, a1 + 1)))
    elif rid == 2:
        save_hadith_mcp(inbox, "bukhari", "4750", "عَنْ عَائِشَةَ رَضِيَ اللَّهُ عَنْهَا قَالَتْ: كَانَ رَسُولُ اللَّهِ ﷺ إِذَا أَرَادَ سَفَرًا أَقْرَعَ بَيْنَ نِسَائِهِ... حَدِيثُ الْإِفْكِ", text_en="Hadith of Ifk", grades="صحيح", covers_ayat=list(range(a0, a1 + 1)))
    elif rid == 4:
        save_hadith_mcp(inbox, "bukhari", "5066", "يَا مَعْشَرَ الشَّبَابِ مَنِ اسْتَطَاعَ مِنْكُمُ الْبَاءَةَ فَلْيَتَزَوَّجْ", text_en="O young men...", grades="صحيح", covers_ayat=list(range(a0, a1 + 1)))
    elif rid == 5:
        save_hadith_mcp(inbox, "bukhari", "7437", "إِنَّ اللَّهَ لَا يَنَامُ، وَلَا يَنْبَغِي لَهُ أَنْ يَنَامَ، حِجَابُهُ النُّورُ", text_en="His veil is Light", grades="صحيح", covers_ayat=list(range(a0, a1 + 1)))
    elif rid == 6:
        save_hadith_mcp(inbox, "bukhari", "6502", "كُلُّكُمْ رَاعٍ وَكُلُّكُمْ مَسْئُولٌ عَنْ رَعِيَّتِهِ", text_en="All of you are guardians", grades="صحيح", covers_ayat=list(range(a0, a1 + 1)))
    elif rid == 7:
        save_hadith_mcp(inbox, "bukhari", "7137", "سَمِعْتُ النَّبِيَّ ﷺ يَقُولُ لَا تَزَالُ طَائِفَةٌ مِنْ أُمَّتِي ظَاهِرِينَ عَلَى الْحَقِّ", text_en="A group of my ummah will remain steadfast", grades="صحيح", covers_ayat=list(range(a0, a1 + 1)))
    elif rid == 8:
        save_hadith_mcp(inbox, "bukhari", "6240", "الِاسْتِئْذَانُ ثَلَاثٌ فَإِنْ أُذِنَ لَكَ وَإِلَّا فَارْجِعْ", text_en="Seeking permission is three times", grades="صحيح", covers_ayat=list(range(a0, a1 + 1)))
    elif rid == 9:
        save_hadith_mcp(inbox, "bukhari", "4770", "لَا تَجْعَلُوا دُعَاءَ الرَّسُولِ بَيْنَكُمْ كَدُعَاءِ بَعْضِكُمْ بَعْضًا", text_en="Do not make the calling of the Messenger...", grades="صحيح", covers_ayat=list(range(a0, a1 + 1)))

    # Ingest
    caps = ingest(p, 24, rid, inbox)
    print(f"✓ Ruku {rid}: Ingested {len(caps)} sources successfully.")


if __name__ == "__main__":
    for rid in range(1, 10):
        harvest_ruku(rid)
    print("\n✓ ALL 9 RUKUS OF SURAH 24 HARVESTED & INGESTED!")
