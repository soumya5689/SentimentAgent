from googleapiclient.discovery import build

def fetch_videos(api_key, query, max_results=20):
    youtube = build("youtube", "v3", developerKey=api_key)
    req = youtube.search().list(q=query, part="snippet", type="video", maxResults=max_results)
    res = req.execute()

    videos = []
    for item in res["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        description = item["snippet"]["description"]
        channel = item["snippet"]["channelTitle"]

        # Get statistics
        stats = youtube.videos().list(part="statistics", id=video_id).execute()
        stats_data = stats["items"][0]["statistics"]

        videos.append({
            "videoId": video_id,
            "title": title,
            "description": description,
            "channelTitle": channel,
            "views": int(stats_data.get("viewCount", 0)),
            "likes": int(stats_data.get("likeCount", 0))
        })
    return videos


def fetch_comments(api_key, video_id, max_comments=50):
    youtube = build("youtube", "v3", developerKey=api_key)
    comments = []
    req = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=50, textFormat="plainText")
    res = req.execute()

    for item in res.get("items", []):
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)

    return comments
