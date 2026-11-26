# উৎস-ক্যাপচার (inbox) বিন্যাস ও হারভেস্ট-নির্দেশনা

পাইপলাইনের লেখক-এজেন্টরা কোনো MCP/ইন্টারনেট টুল পায় না। তারা শুধু `jp ingest` দিয়ে নিবন্ধিত ক্যাপচার পড়ে। ক্যাপচার সংগ্রহ (harvest) আপনার বিদ্যমান টুলে (Antigravity-র MCP: `turath`, `bahouth`) হয়; এখানে শুধু ফাইলের বিন্যাস ঠিক করা আছে।

> **নীতি:** MCP-র আউটপুট **হুবহু** সেভ করুন — সারসংক্ষেপ/সম্পাদনা/অনুবাদ নয়। `sha256` প্রমাণ করে ingest-এর পর টেক্সট বদলায়নি; মূল উৎসের খাঁটিত্ব নির্ভর করে এই ধাপের সততার ওপর।

## ১. Turath পৃষ্ঠা (সবচেয়ে সহজ: `.txt`)
ফাইলের নাম: `turath_<বই-আইডি>_<পৃষ্ঠা-আইডি>_a<শুরু>-<শেষ>.txt` (একটি আয়াত হলে `_a5.txt`; পুরো সূরা-ব্যাপী `_asurah.txt`)। ভেতরে শুধু পৃষ্ঠার টেক্সট।
উদাহরণ: `turath_7798_11962_a3-4.txt`

অভ্যন্তরীণ পৃষ্ঠা-নম্বর (`internalPage`) সংরক্ষণ করতে JSON ব্যবহার করুন:
```json
{
  "kind": "turath_page",
  "book_id": 7798,
  "page_id": 11962,
  "internal_page": "১৭/১১৯৬২",
  "covers_ayat": [3, 4],
  "text": "… MCP-র টেক্সট হুবহু …",
  "tool": "turath:retrieve",
  "args": {"book_id": 7798, "query": "…"}
}
```
`book_id` অবশ্যই `pipeline/books.json`-এর `allowed`-এ থাকতে হবে; `blocked` (যেমন ২১৫৪৩) প্রত্যাখ্যাত হয়।

## ২. বাহাউথ
**কিরাআত (সহজ উপায়):** আপনার বিদ্যমান `_sources/ruku_XX_raw.json` (schema `2.0-raw-mcp`) বা `ruku_XX_qiraat_table.md` সরাসরি inbox-এ রাখুন — ingest দুটোই বোঝে (`bahouth_verses` + `bahouth_qiraat` থেকে স্বাধীন আয়াত-যাচাই ও কিরাআত-সারি দুটোই নেওয়া হয়)।

**envelope JSON:**
```json
{"kind": "bahouth_qiraat", "rows": [
  {"ayah": 4, "word_cell": "﴿كُفُوًا﴾ (5)", "readers": "حمزة", "rule": "قرأ بإسكان الفاء."}
]}
```
```json
{"kind": "bahouth_verses", "verses": [{"ayah": 1, "text_raw": "قل هو الله أحد"}]}
```
```json
{"kind": "bahouth_root", "root": "احد", "covers_ayat": "surah",
 "text": "root: احد | কুরআনে মোট: 85 | স্বতন্ত্র আয়াত: …"}
```
মূলধাতুর গণনা (`bahouth_root`) না দিলে মুফরাদাত-সারণির গণনা-কলামে `যাচাইসাপেক্ষ` লেখা বাধ্যতামূলক হবে — অনুমান করে সংখ্যা বসবে না।

## ৩. মাল্টি-এমসিপি এনভেলপ (Multi-MCP Envelopes)
### ৩.১ শামেলা পৃষ্ঠা (`shamela_page`)
```json
{
  "kind": "shamela_page",
  "book_id": 23635,
  "page": 167,
  "volume": 32,
  "book_title": "مفاتيح الغيب (التفسير الكبير)",
  "author": "فخر الدين الرازي",
  "role": "tafsir",
  "covers_ayat": [1, 2, 3, 4],
  "text": "… MCP-র মূল আরবি টেক্সট হুবহু …",
  "url": "https://shamela.ws/book/23635/167"
}
```

### ৩.২ তাফসীর সেন্টার (`tafsir_mcp`)
```json
{
  "kind": "tafsir_mcp",
  "subtype": "tafsir",
  "key": "112-1",
  "source_name": "تفسير الطبري",
  "author": "ابن جرير الطبري",
  "role": "tafsir",
  "covers_ayat": [1],
  "text": "… হুবহু তাফসীর পাঠ …"
}
```

### ৩.৩ হাদীস ও তাখরীজ (`hadith_mcp` ও `maher_hadith`)
```json
{
  "kind": "hadith_mcp",
  "collection": "bukhari",
  "hadith_number": "5013",
  "chapter_title": "فضل قل هو الله أحد",
  "text_ar": "… حَدَّثَنَا … أَنَّ رَجُلاً سَمِعَ رَجُلاً يَقْرَأُ ﴿قُلْ هُوَ اللَّهُ أَحَدٌ﴾ …",
  "grades": "صحيح البخاري",
  "cross_refs": ["muslim:811", "abudawud:1461"],
  "covers_ayat": [1, 2, 3, 4]
}
```

## ৪. ফিকহ-গ্রন্থ ও ফতোয়া (আহকাম ও সমকালীন দরস)
`books.json`-এ `"role": "fiqh"` এন্ট্রি যোগ করে (হিদায়াহ, বাদা'ই', মুদাওওয়ানাহ, উম্ম, মাজমূ', মুগনী…) §১-এর মতো `turath_page` ক্যাপচার দিন; অথবা `fiqh_fatwa` এনভেলপ দিন।

## ৫. IDE-এজেন্টকে দেওয়ার হারভেস্ট-প্রম্পট (কপি করুন)
```
তুমি শুধু ডেটা-সংগ্রাহক। pipeline/jp.py harvest-plan দিয়ে তৈরি
_work/s<সূরা>/r<রুকু>/harvest_requests.json পড়ো। প্রতিটি অনুরোধের জন্য সংশ্লিষ্ট MCP টুল
(turath:retrieve, bahouth:list_verse_qiraat, list_surah_verses, find_root) চালাও এবং আউটপুট
HUBOHU (verbatim) <inbox>/ ফোল্ডারে docs/INBOX_FORMAT.md-এর নাম/বিন্যাসে সেভ করো।
কোনো সারসংক্ষেপ, অনুবাদ, সংশোধন বা বানানো তথ্য নয়। টুল কিছু না পেলে ফাইল বানিও না এবং
শেষে কোন অনুরোধ অপূর্ণ তার তালিকা দাও।
```
এরপর: `python pipeline/jp.py ingest --surah S --ruku R --inbox <inbox>`।
