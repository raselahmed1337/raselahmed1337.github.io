#!/usr/bin/env python3
import json, os, re, requests, sys

UID   = "1qLYFGYAAAAJ"   # <--- your Scholar ID
URL   = f"https://scholar.google.com/citations?user={UID}&hl=en&cstart=0&pagesize=100"
HEAD  = {"User-Agent": "Mozilla/5.0 (compatible; GitHub-ScholarBot/1.0)"}

html  = requests.get(URL, headers=HEAD, timeout=30).text
papers = []
for row in re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', html, re.DOTALL):
    title  = re.search(r'class="gsc_a_at">(.*?)</a>', row).group(1)
    auth   = re.search(r'<div class="gs_gray">(.*?)</div>', row).group(1)
    venue  = re.search(r'</div><div class="gs_gray">(.*?)</div>', row)
    venue  = venue.group(1) if venue else ""
    year   = re.search(r'class="gsc_a_y">(.*?)</span>', row).group(1)
    link   = "https://scholar.google.com" + re.search(r'href="(/citations[^"]+)"', row).group(1)
    papers.append({"title": title, "authors": auth, "venue": venue, "year": year, "link": link})

os.makedirs("_data", exist_ok=True)
json.dump(papers, open("_data/scholar.json", "w", encoding="utf-8"), indent=2)
print(f"✅  {len(papers)} papers → _data/scholar.json")
