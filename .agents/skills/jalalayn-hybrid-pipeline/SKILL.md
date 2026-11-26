---
name: jalalayn-hybrid-pipeline
description: >-
  জালালাইন তাহকীক গবেষণা প্রকল্পের আন্তর্জাতিক মানের হাইব্রিড ত্রি-স্তর Smart Core 7
  মাল্টি-এমসিপি সাব-এজেন্ট পাইপলাইন পরিচালনার মাস্টার স্কিল। যেকোনো সূরা ও রুকুর জন্য
  ৫-বিশেষজ্ঞ হারভেস্টার, ৯-স্কিল লেখক দল, যান্ত্রিক যাচাই, মার্জ, অডিট ও ওয়েব সিঙ্ক সম্পন্ন করে।
---

# মাস্টার স্কিল: জালালাইন হাইব্রিড ত্রি-স্তর Smart Core 7 সাব-এজেন্ট পাইপলাইন

এই মাস্টার স্কিলটি **আন্তর্জাতিক ইসলামী একাডেমিক মানদণ্ডে** (মারকায তাফসীর, আল-আযহার ও দারসে নেযামী তাহক্বীক মান) ১৬ অধ্যায়ের জালালাইন মুফাস্সির ক্লাস নোট ও গবেষণা-রুকু প্রস্তুত করার সম্পূর্ণ ত্রি-স্তর স্বয়ংক্রিয় সাব-এজেন্ট দল পরিচালনা করে।

## ত্রি-স্তর স্থাপত্য (3-Tier Academic Architecture)

1. **Tier 1 — ৫-সদস্যের মাল্টি-এমসিপি হারভেস্টার দল (`Smart Core 7`):**
   - সক্রিয় সার্ভার: `turath`, `bahouth`, `tafsir-center`, `quran-mcp`, `shamela-qg`, `hadith-mcp`, `maher-alfahel`।
   - ৫ জন বিশেষায়িত হারভেস্টার (`harvester-quran-qiraat`, `harvester-jalalayn-tafsir`, `harvester-hadith-nuzul`, `harvester-lughah-balaghat`, `harvester-fiqh-aqidah`) সমান্তরালে হুবহু (verbatim) আরবি ইবারত, কিরাআত, সনদ ও তাখরীজ সংগ্রহ করে `_work/sNNN/rNN/inbox/`-এ সেভ করে এবং `jp.py ingest` দিয়ে `SHA-256` সিল করে।
   - বিস্তারিত প্রটোকল: `.agents/skills/jalalayn-harvester/SKILL.md`।
2. **Tier 2 — ৯টি স্কিলের জিরো-টুল একাডেমিক লেখক দল (৩টি নির্ভরশীল স্তর):**
   - কোনো লেখক সাব-এজেন্টের হাতে ইন্টারনেট বা MCP টুল থাকে না (Strict Epistemic Isolation); তারা কেবল সিলকৃত `SRC` ও `PRIOR_OUTPUTS` থেকে লিখে।
   - **Level 1 (সমান্তরাল আয়াত ও তাফসীর-ইউনিট):** `ayah-translation-jalalayn` (§১, §৫খ), `ayah-lughah-irab` (§২, §৩), `ayah-qiraat-note` (§৪ মন্তব্য), `tafsir-hadith-unit` (§৫ক, §৬)।
   - **Level 2 (সমান্তরাল সামষ্টিক রুকু):** `ruku-makasid-connections` (§০, §১২), `ruku-ikhtilaf-ahkam` (§৭, §৮), `ruku-ulum-balaghat` (§৯, §১০)।
   - **Level 3 (সমান্তরাল দরস ও স্বচ্ছতা):** `ruku-samakalin-dars` (§১১, §১৩), `ruku-limitations` (§১৫)।
   - প্রতিটি আউটপুট `jp.py submit-part` (`validate.py`) দিয়ে যাচাই হয়; ত্রুটি পেলে সর্বোচ্চ ৩ বার বাংলা ত্রুটি-তালিকাসহ স্বয়ংক্রিয় সংশোধন লুপ চলে।
3. **Tier 3 — LLM-মুক্ত যান্ত্রিক গেটকিপার ও ওয়েব প্রকাশনা:**
   - `jp.py merge`: Tanzil মূল আয়াত + Bahouth ১০ কিরাআত সারণি + **মাল্টি-সার্ভার অটো-গ্রন্থপঞ্জি (§১৪)** সহ ১৬-অধ্যায়ের চূড়ান্ত রুকু `.md` তৈরি করে।
   - `jp.py audit`: SHA-256 হ্যাশ, উদ্ধৃতি-সাবস্ট্রিং, সূত্র-সংখ্যা, কুরআন-রেফ, জালালাইন-রচয়িতা ও ক্বারী-নাম পরীক্ষা করে **`digital_verified`** (`0 errors`) প্রদান করে।
   - `jp.py approve --by "<নাম>"`: মানবিক/মুফতী পর্যায়ের পর্যালোচনার পর **`gold`** সিল (+ ফাইল বদলালে স্বয়ংক্রিয় tamper detection)।
   - `python scripts/build_web_data.py --surah <S>`: ওয়েব অ্যাপে সিঙ্ক।

---

## চালনার দুটি অনুমোদিত পদ্ধতি (Dual Orchestration Modes)

### পদ্ধতি ক: সম্পূর্ণ স্বয়ংক্রিয় ডাইনামিক ওয়ার্কফ্লো (`run_workflow` — প্রস্তাবিত)
এক কমান্ডে Tier 1 (৫ হারভেস্টার প্যারালাল) → Tier 2 (৩ লেভেল প্যারালাল + অটো-ফিডব্যাক) → Tier 3 (মার্জ ও অডিট) চালাতে:

```python
run_workflow(
    ScriptPath="d:/আমার গবেষণা/জালালাইন/pipeline/workflow_ruku.py",
    Description="সূরা <S> রুকু <R> Smart Core 7 মাল্টি-এমসিপি তাহক্বীক",
    Args={"surah": 112, "ruku": 1, "skip_harvest": False, "force": False, "model_tier": "inherit"}
)
```

### পদ্ধতি খ: ধাপে ধাপে ইন্টারেক্টিভ সাব-এজেন্ট / CLI মোড
যখন গবেষক প্রতিটি ধাপ সরাসরি পর্যবেক্ষণ করতে চান:

```powershell
# ১. হারভেস্ট প্ল্যান তৈরি
python pipeline/jp.py harvest-plan --surah <S> --ruku <R>

# ২. (৫ হারভেস্টার সাব-এজেন্ট দিয়ে inbox/ ভরার পর) SHA-256 সিলিং
python pipeline/jp.py ingest --surah <S> --ruku <R> --inbox _work/s<S>/r<R>/inbox

# ৩. প্রতিটি লেভেলের প্রম্পট তৈরি ও যাচাইকৃত সাবমিশন (level = 1, 2, 3)
python pipeline/jp.py prepare-level --surah <S> --ruku <R> --level 1
python pipeline/jp.py submit-part --surah <S> --ruku <R> --task "<task_id>" --file "<draft_path>"

# ৪. LLM-মুক্ত মার্জ, অডিট ও ওয়েব সিঙ্ক
python pipeline/jp.py merge --surah <S> --ruku <R>
python pipeline/jp.py audit --surah <S> --ruku <R>
python scripts/build_web_data.py --surah <S>

# ৫. মুফতী/গবেষকের মানবিক পর্যালোচনার পর Gold অনুমোদন
python pipeline/jp.py approve --surah <S> --ruku <R> --by "মুফতী মুহাম্মাদ মুহিব্বুল্লাহ"
```

---

## একাডেমিক মাননিয়ন্ত্রণ চেকলিস্ট (Quality Gate)
- [ ] `python -m unittest discover -s pipeline/tests -v` — সব ইউনিট টেস্ট ১০০% পাস।
- [ ] `python pipeline/jp.py validate-map` — রুকু মানচিত্র Tanzil-এর সাথে নির্ভুল।
- [ ] চূড়ান্ত রুকু অডিটে `status: digital_verified`, `errors: []` নিশ্চিত।
- [ ] অধ্যায় ১৪-এ ব্যবহৃত সব Smart Core 7 উৎসের (`Turath`, `Shamela`, `Tafsir Center`, `Hadith MCP`, `Maher Al-Fahel`, `Quran.com`, `Bahouth`) প্রামাণ্য গ্রন্থপঞ্জি উপস্থিত।
