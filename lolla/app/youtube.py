"""Methods that use the YouTube API to find and embed artist top videos."""

import os
import requests
from dash import html

def get_youtube_video_id(artist_name: str) -> str:
    """Searches for the most relevant embeddable YouTube video for the given artist."""
    print(f"Searching for YouTube video for artist: {artist_name}")

    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("Missing YOUTUBE_API_KEY environment variable")

    query = f"{artist_name} band music video"
    search_url = "https://www.googleapis.com/youtube/v3/search"
    video_url = "https://www.googleapis.com/youtube/v3/videos"

    search_params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 10,
        "key": api_key,
        "videoEmbeddable": "true",
        "videoSyndicated": "true",
        "safeSearch": "none",
    }

    response = requests.get(search_url, params=search_params)
    if response.status_code != 200:
        raise Exception(f"YouTube API error: {response.status_code}, {response.text}")

    items = response.json().get("items", [])
    if not items:
        return None

    # Exclude live concerts or features
    exclude_keywords = ["live", "concert", "feat", "ft." "featuring"]
    items = [
        item for item in items
        if not any(keyword in item["snippet"]["title"].lower() for keyword in exclude_keywords)
    ]

    video_ids = [item["id"]["videoId"] for item in items]

    # Check embeddability of each video
    for video_id in video_ids:
        detail_params = {
            "part": "status",
            "id": video_id,
            "key": api_key,
        }
        detail_response = requests.get(video_url, params=detail_params)
        if detail_response.status_code == 200:
            details = detail_response.json().get("items", [])
            if details and details[0]["status"].get("embeddable", False):
                return video_id

    # No embeddable video found
    return None

def create_youtube_embed(video_id: str, width: str = "560", height: str = "315") -> html.Iframe:
    """Creates a Dash HTML iframe component for embedding a YouTube video."""
    if not video_id:
        return html.Div("No video available.")
    return html.Iframe(
        src=f"https://www.youtube.com/embed/{video_id}?autoplay=1",
        width=width,
        height=height,
        style={"border": "none"},
        referrerPolicy="no-referrer-when-downgrade",
        allow="autoplay; encrypted-media",
    )

if __name__ == "__main__":
    artist_name = "Charlotte Lawrence"
    video_id = get_youtube_video_id(artist_name)
    if video_id:
        print(f"Video ID for {artist_name}: {video_id}")
    else:
        print(f"No video found for {artist_name}")

    create_youtube_embed(video_id)