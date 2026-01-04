import os
import requests

API_KEY = os.environ.get("YOUTUBE_API_KEY")
VIDEO_ID = "VIDEO_ID_DALO"
KEYWORD = "nice"

comments = []
page = ""

while True:
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": VIDEO_ID,
        "maxResults": 100,
        "pageToken": page,
        "key": API_KEY
    }

    data = requests.get(url, params=params).json()

    for item in data.get("items", []):
        c = item["snippet"]["topLevelComment"]["snippet"]
        comments.append({
            "text": c["textDisplay"],
            "likes": c["likeCount"]
        })

    page = data.get("nextPageToken")
    if not page:
        break

best = None
for c in comments:
    if KEYWORD in c["text"].lower():
        if best is None or c["likes"] > best["likes"]:
            best = c

print(best)
