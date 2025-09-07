from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import matplotlib 
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import io, base64, os
from youtube_api import fetch_videos, fetch_comments
from sentiment import analyze_sentiment

API_KEY = ""

app = FastAPI(title="Atomberg Share of Voice API")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["http://127.0.0.1:5173"],
)

# Temporary CSV path
CSV_PATH = "results.csv"

# Convert matplotlib figure to base64 string
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return img_str


@app.get("/analyze")
def analyze(query: str = Query(..., description="Search keyword"),
            results: int = Query(20, description="Number of YouTube results")):
    
    videos = fetch_videos(API_KEY, query, results)
    all_data = []

    for vid in videos:
        comments = fetch_comments(API_KEY, vid["videoId"])
        sentiment_score = analyze_sentiment(" ".join(comments))

        all_data.append({
            "title": vid["title"],
            "channel": vid["channelTitle"],
            "views": vid["views"],
            "likes": vid["likes"],
            "mentions_atomberg": "atomberg" in vid["title"].lower() or "atomberg" in vid["description"].lower(),
            "sentiment": sentiment_score
        })

    df = pd.DataFrame(all_data)

    # Save CSV
    df.to_csv(CSV_PATH, index=False)

    # Share of Voice
    atomberg_mentions = df[df["mentions_atomberg"] == True]
    sov = (len(atomberg_mentions) / len(df)) * 100

    # Chart 1: Pie
    labels = ["Atomberg", "Others"]
    sizes = [len(atomberg_mentions), len(df) - len(atomberg_mentions)]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")
    pie_chart = fig_to_base64(fig1)

    # Chart 2: Bar
    fig2, ax2 = plt.subplots()
    ax2.bar(df["channel"], df["sentiment"], color="skyblue")
    ax2.set_xlabel("Channels")
    ax2.set_ylabel("Sentiment Score")
    ax2.set_title("Sentiment Analysis of Top Videos")
    plt.xticks(rotation=45, ha="right")
    bar_chart = fig_to_base64(fig2)

    return {
        "query": query,
        "total_results": len(df),
        "share_of_voice": round(sov, 2),
        "videos": all_data,
        "charts": {
            "pie_chart": pie_chart,
            "bar_chart": bar_chart
        },
        "csv_download_url": "/download_csv"
    }


@app.get("/download_csv")
def download_csv():
    if os.path.exists(CSV_PATH):
        return FileResponse(
            path=CSV_PATH,
            filename="results.csv",
            media_type="text/csv"
        )
    return {"error": "CSV not found. Run /analyze first."}
