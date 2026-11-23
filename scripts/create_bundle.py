import os
from pathlib import Path

BASE_DIR = Path(r"d:\আমার গবেষণা\জালালাইন")
OUTPUT_FILE = BASE_DIR / "temp_web_pipeline_bundle.md"

files_to_bundle = [
    {
        "id": "1",
        "title": "১. ডেটা বিল্ডার স্ক্রিপ্ট (build_web_data.py)",
        "path": BASE_DIR / "scripts" / "build_web_data.py",
        "lang": "python",
        "desc": "মূল .md ফাইলগুলো থেকে ১৬টি শাস্ত্রীয় অধ্যায়, তরজমা, মুফরাদাত, কিরাআত, জালালাইন ও ফিকহ টেবিল পার্স করে public/data-তে ruku-X.json তৈরি করে।"
    },
    {
        "id": "2",
        "title": "২. অধ্যায়ের বডি প্রদর্শনকারী মূল ফ্রন্টএন্ড ভিউ (ThematicView.jsx)",
        "path": BASE_DIR / "web" / "src" / "components" / "ThematicView.jsx",
        "lang": "jsx",
        "desc": "অধ্যায় ০ থেকে ১৫-এর নেভিগেশন সাইডবার ও ড্রপডাউন পরিচালনা করে; MarkdownContent ও MasalaCard রেন্ডার করে।"
    },
    {
        "id": "3",
        "title": "৩. রেন্ডার পাইপলাইন ও আরবি-র‍্যাপিং DOM TreeWalker (MarkdownContent.jsx)",
        "path": BASE_DIR / "web" / "src" / "components" / "MarkdownContent.jsx",
        "lang": "jsx",
        "desc": "Marked ও DOMPurify-এর পর DOM TreeWalker চালিয়ে সব আরবি টেক্সট ও ﴿﴾ ব্র্যাকেটকে <bdi dir='rtl'>-এ মোড়ায়।"
    },
    {
        "id": "4",
        "title": "৪. আরবি ও কুরআনিক ব্র্যাকেট আইসোলেশন ইউটিলিটি (bidiRenderer.jsx)",
        "path": BASE_DIR / "web" / "src" / "utils" / "bidiRenderer.jsx",
        "lang": "jsx",
        "desc": "﴿...﴾ ও «...» উদ্ধৃতিগুলোকে রিঅ্যাক্ট লেভেলে আইসোলেটেড BiDi বাউন্ডারিতে রেন্ডার করার হেল্পার।"
    },
    {
        "id": "5",
        "title": "৫. ৪ মাযহাবের তুলনামূলক ফতোয়া ও দলীল কার্ড (MasalaCard.jsx)",
        "path": BASE_DIR / "web" / "src" / "components" / "MasalaCard.jsx",
        "lang": "jsx",
        "desc": "অধ্যায় ৮-এর হানাফী, মালিকী, শাফিঈ ও হাম্বলী মাযহাবের ফতোয়া গ্রিড, ইজমা/মতভেদ ব্যাজ এবং দলিলসমূহ প্রদর্শন করে।"
    },
    {
        "id": "6",
        "title": "৬. সম্পূর্ণ সিএসএস, থিম ও টাইপোগ্রাফি স্টাইলিং (index.css)",
        "path": BASE_DIR / "web" / "src" / "index.css",
        "lang": "css",
        "desc": "Tailwind বেস, ডার্ক/লাইট/সেপিয়া থিম ভেরিয়েবল, .prose ও আরবি ফন্ট সেটিংস।"
    },
    {
        "id": "7",
        "title": "৭. মার্কডাউন রেন্ডারিং রিগ্রেশন টেস্ট স্যুট (test_markdown_rendering.mjs)",
        "path": BASE_DIR / "scripts" / "test_markdown_rendering.mjs",
        "lang": "javascript",
        "desc": "২৫৯টি রুকুর সকল কনটেন্ট পার্স করে কাঁচা মার্কডাউন লিক (যেমন |---|, <br>, ###) খোঁজে।"
    },
    {
        "id": "8",
        "title": "৮. ওয়েব ডেটা অখণ্ডতা ও উসমানী লিপি যাচাইকারী (verify_web_data.py)",
        "path": BASE_DIR / "scripts" / "verify_web_data.py",
        "lang": "python",
        "desc": "৯১টি সূরা, ৩,৪৪৫ আয়াত এবং ২৫৯টি রুকুর JSON ফাইলের সম্পূর্ণতা ও উসমানী আরবির অস্তিত্ব অডিট করে।"
    }
]

lines = []
lines.append("# মুফাস্সির ক্লাস নোট — ওয়েব পাইপলাইন ও ফ্রন্টএন্ড কোড বান্ডল (অস্থায়ী সংকলন)")
lines.append("")
lines.append("> **নোট:** ব্যবহারকারীর পর্যালোচনা, অফলাইন টেস্ট ও রিগ্রেশন পরীক্ষার সুবিধার্থে ফ্রন্টএন্ড রেন্ডারিং পাইপলাইন, বিল্ড স্ক্রিপ্ট ও টেস্ট স্যুট এই একক ফাইলে সমন্বিত করা হলো।")
lines.append("")
lines.append("## সূচিপত্র (Table of Contents)")
lines.append("")

for item in files_to_bundle:
    rel_p = str(item["path"].relative_to(BASE_DIR)).replace("\\", "/")
    lines.append(f"- [{item['title']}](#{item['id']}) — `{rel_p}`")

lines.append("")
lines.append("---")
lines.append("")

for item in files_to_bundle:
    rel_p = str(item["path"].relative_to(BASE_DIR)).replace("\\", "/")
    content = item["path"].read_text(encoding="utf-8")
    
    lines.append(f"<a id='{item['id']}'></a>")
    lines.append(f"## {item['title']}")
    lines.append(f"- **লোকাল পাথ:** `{rel_p}`")
    lines.append(f"- **বিবরণ:** {item['desc']}")
    lines.append("")
    lines.append(f"```{item['lang']}")
    lines.append(content)
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")

OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
print(f"Successfully generated: {OUTPUT_FILE} (Size: {OUTPUT_FILE.stat().st_size} bytes)")
