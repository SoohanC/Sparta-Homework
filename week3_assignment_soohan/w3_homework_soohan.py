import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# DB
client = MongoClient('localhost', 27017)
db = client.dbsparta
# REQUEST
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
chart_date = 20201010
data = requests.get(f"https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd={chart_date}", headers=headers)

# PROCESS
soup = BeautifulSoup(data.text, 'html.parser')
songs = soup.select("#body-content > div.newest-list > div > table > tbody > tr")

for song in songs:
    rank = song.select_one(".number").text[0:2].strip()
    title = song.select_one(".title").text.strip()
    artist = song.select_one(".artist").text.strip()
    db_data = {
        "rank": rank, "title": title, "artist": artist,
    }
    db.genie.insert_one(db_data)

# CONFIRM
all_data = list(db.genie.find({}))
for item in all_data:
    rank = item["rank"]
    title = item["title"]
    artist = item["artist"]
    print(rank, title, artist)
