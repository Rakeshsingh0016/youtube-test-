from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)

API_KEY = os.environ.get("YOUTUBE_API_KEY")

def get_comments(video_id, keyword):
    comments = []
    page_token = ""

    while True:
        url = "https://www.googleapis.com/youtube/v3/commentThreads"
        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": 100,
            "pageToken": page_token,
            "key": API_KEY
        }

        res = requests.get(url, params=params).json()

        for item in res.get("items", []):
            c = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "text": c["textDisplay"],
                "likes": c["likeCount"],
                "author": c["authorDisplayName"]
            })

        page_token = res.get("nextPageToken")
        if not page_token:
            break

    # Filter keyword + highest like
    best = None
    for c in comments:
        if keyword.lower() in c["text"].lower():
            if best is None or c["likes"] > best["likes"]:
                best = c
    return best

@app.route("/get_comment")
def get_comment():
    video_id = request.args.get("video")
    keyword = request.args.get("keyword", "nice")
    result = get_comments(video_id, keyword)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
