import os
import requests
import random

from dash import html

def get_youtube_video_id(artist_name: str, results_to_choose: int = 3) -> str:
    """Searches for the most relevant embeddable YouTube video for the given artist."""
    print(f"Searching for YouTube video for artist: {artist_name}")

    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("Missing YOUTUBE_API_KEY environment variable")

    query = f"{artist_name} band music video"
    search_url = "https://www.googleapis.com/youtube/v3/search"

    search_params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": results_to_choose,
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

    selected_video = random.choice(items)
    return selected_video["id"]["videoId"]

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

    print("Done")