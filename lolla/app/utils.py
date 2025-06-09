import base64
import pandas as pd
from pathlib import Path

from lolla.scheduling.constants import STAGES
from lolla.scheduling.artists import Artist


def get_schedule_background_image_b64() -> str:
    """Get the background image as a base64 encoded string for CSS use."""
    background_image_path = Path(__file__).parent.parent.parent / "resources" / "schedule_background.png"
    with open(background_image_path, "rb") as f:
        img_bytes = f.read()
    return base64.b64encode(img_bytes).decode()


def get_landing_page_background_image_b64() -> str:
    """Get the landing page background image as a base64 encoded string for CSS use."""
    background_image_path = Path(__file__).parent.parent.parent / "resources" / "landing_page_background.jpg"
    with open(background_image_path, "rb") as f:
        img_bytes = f.read()
    return base64.b64encode(img_bytes).decode()


def serialize_schedule_df(schedule_df: pd.DataFrame) -> list[dict]:
    """Convert DataFrame with Artist objects to serializable format."""
    data = []
    for _, row in schedule_df.iterrows():
        row_data = {}
        for stage in STAGES:
            artist = row[stage]
            if isinstance(artist, Artist):
                row_data[stage] = artist.to_dict()
            else:
                row_data[stage] = None
        data.append(row_data)
    return data


def deserialize_schedule_df(schedule_data: list[dict]) -> pd.DataFrame:
    """Convert serializable format back to DataFrame with Artist objects."""
    from lolla.scheduling.constants import HOURS

    rows = []
    for row_data in schedule_data:
        row = {}
        for stage in STAGES:
            artist_data = row_data.get(stage)
            if artist_data:
                row[stage] = Artist.from_dict(artist_data)
            else:
                row[stage] = None
        rows.append(row)

    schedule_df = pd.DataFrame(rows, columns=STAGES)
    schedule_df.index = HOURS[: len(schedule_df)]
    return schedule_df