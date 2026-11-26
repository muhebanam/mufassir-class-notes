"""সূরা ১১২ রুকু ১-এর সোর্স হার্ভেস্ট ও ইনবক্স সেভিং স্ক্রিপ্ট।"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))

from harvester_helper import (
    prepare_inbox_from_existing,
    save_bahouth_root,
    save_turath_page,
)
from jalalayn_pipeline.config import Config
from jalalayn_pipeline.project import Project

inbox = ROOT / "_work" / "s112" / "r01" / "inbox"
inbox.mkdir(parents=True, exist_ok=True)
proj = Project(Config(base_dir=ROOT))

# 1. Existing raw & qiraat
prep = prepare_inbox_from_existing(proj, 112, 1, inbox)
print("Copied existing files:", prep["copied_legacy_files"])

# 2. Jalalayn 12876
jal_text = """النَّبِيّ ﷺ عَنْ رَبّه فَنَزَلَ ﴿قُلْ هُوَ اللَّه أَحَد﴾ فَاَللَّه خَبَر هُوَ وَأَحَد بَدَل مِنْهُ أَوْ خَبَر ثَانٍ

﴿اللَّه الصَّمَد﴾ مُبْتَدَأ وَخَبَر أَيْ الْمَقْصُود فِي الْحَوَائِج عَلَى الدَّوَام

﴿لَمْ يَلِد﴾ لِانْتِفَاءِ مُجَانَسَته ﴿وَلَمْ يُولَد﴾ لِانْتِفَاءِ الحدوث عنه

﴿وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَد﴾ أَيْ مُكَافِئًا وَمُمَاثِلًا وَلَهُ مُتَعَلِّق بِكُفُوًا وَقُدِّمَ عَلَيْهِ لِأَنَّهُ مَحَطّ الْقَصْد بِالنَّفْيِ وَأُخِّرَ أَحَد وَهُوَ اِسْم يكن عن خبرها رعاية للفاصلة"""

save_turath_page(
    inbox, book_id=12876, page_id=6920, internal_page="1/826",
    covers_ayat=[1, 2, 3, 4], text=jal_text, tool="turath:get_context"
)

# 3. Tabari 7798
tab_text = """تفسير سورة الإخلاص
القول في تأويل قوله جل ثناؤه وتقدست أسماؤه: ﴿قُلْ هُوَ اللَّهُ أَحَدٌ (١) اللَّهُ الصَّمَدُ (٢) لَمْ يَلِدْ وَلَمْ يُولَدْ (٣) وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ (٤)﴾.
ذُكر أن المشركين سألوا رسول الله ﷺ عن نسب رب العزة، فأنزل الله هذه السورة جوابا لهم. وقال بعضهم: بل نزلت من أجل أن اليهود سألوه، فقالوا له: هذا الله خلق الخلق، فمن خلق الله؟ فأنزلت جوابا لهم.
حدثنا أحمد بن منيع ومحمود بن خداش، قالا: ثنا أبو سعد الصغاني، قال: ثنا أبو جعفر الرازي، عن الربيع بن أنس، عن أبي العالية، عن أبي بن كعب، قال: قال المشركون للنبي ﷺ: انسب لنا ربك. فأنزل الله: ﴿قُلْ هُوَ اللَّهُ أَحَدٌ (١) اللَّهُ الصَّمَدُ﴾."""

save_turath_page(
    inbox, book_id=7798, page_id=16671, internal_page="24/727",
    covers_ayat=[1, 2, 3, 4], text=tab_text, tool="turath:get_context"
)

# 4. Ibn Kathir 8473
ibn_text = """تفسير سورة الإخلاص
وهي مكية. ذكر سبب نزولها وفضيلتها
قال الإمام أحمد: حدثنا أبو سعد محمد بن ميسر الصاغاني، حدثنا أبو جعفر الرازي، حدثنا الربيع بن أنس، عن أبي العالية، عن أبي بن كعب: أن المشركين قالوا للنبي ﷺ: يا محمد، انسب لنا ربك، فأنزل الله: ﴿قُلْ هُوَ اللَّهُ أَحَدٌ * اللَّهُ الصَّمَدُ * لَمْ يَلِدْ وَلَمْ يُولَدْ * وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ﴾.
قال: الصمد الذي لم يلد ولم يولد، لأنه ليس شيء يولد إلا سيموت، وليس شيء يموت إلا سيورث، وإن الله ﷻ لا يموت ولا يورث، ﴿وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ﴾ ولم يكن له شبه ولا عدل، وليس كمثله شيء."""

save_turath_page(
    inbox, book_id=8473, page_id=4564, internal_page="8/518",
    covers_ayat=[1, 2, 3, 4], text=ibn_text, tool="turath:get_context"
)

# 5. Ibn Ashur 9776
ashur_text = """سورة الإخلاص
سورة الإخلاص تسمى في أكثر المصاحف وفي معظم التفاسير وفي جامع الترمذي سورة الإخلاص لما اشتملت عليه من التوحيد الخالص لله تعالى وتنزيهه عن الشريك والولد والنظير والكفء.
وقال تعالى: ﴿قُلْ هُوَ اللَّهُ أَحَدٌ﴾، وهو مبتدأ وأحد خبره، والله الصمد، والصمد السيد الذي يصمد إليه في الحوائج."""

save_turath_page(
    inbox, book_id=9776, page_id=10403, internal_page="30/609",
    covers_ayat=[1, 2, 3, 4], text=ashur_text, tool="turath:get_context"
)

# 6. Roots
save_bahouth_root(inbox, "أحد", "root احد | কুরআনে মোট: 85 | স্বতন্ত্র আয়াত: 85", covers_ayat="surah")
save_bahouth_root(inbox, "صمد", "root صمد | কুরআনে মোট: 1 | স্বতন্ত্র আয়াত: 1", covers_ayat="surah")

print("All sources saved to inbox successfully!")
