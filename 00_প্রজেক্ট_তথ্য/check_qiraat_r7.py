import json, subprocess

# We can call Bahouth tool or inspect qira'at for each verse
# Key qira'at points in 26:69-104 from classical qira'at texts (Tayyibah / Shatibiyyah / Faridat al-Dahr):
# 1. 26:69: إِبْرَاهِيمَ / إِبْرَاهَامَ (Hisham reads with alif in Baqarah, but here all 10 read Ibrahim with ya).
# 2. 26:78: يَهْدِينِ (Ya'qub ithbat ya in waqf and wasl: يَهدِينِي).
# 3. 26:79: يَسْقِينِ (Ya'qub ithbat: يَسقِينِي).
# 4. 26:80: يَشْفِينِ (Ya'qub ithbat: يَشفِينِي).
# 5. 26:81: يُحْيِينِ (Ya'qub ithbat: يُحيِينِي).
# 6. 26:82: خَطِيئَتِي (Ibn Kathir, Abu Amr, etc. read with hamzah/ya; Abu Ja'far reads خَطَايَايَ).
# 7. 26:90: وَأُزْلِفَتِ (All ten read passive).
# 8. 26:91: وَبُرِّزَتِ (All ten read with tashdid).
# 9. 26:94: فَكُبْكِبُوا (All ten read with double kaf).
# 10. 26:102: فَنَكُونَ (Nasb in jawab al-tamanni).

print("Qira'at points identified.")
