import base64
from pathlib import Path
import pandas as pd
from pandas._libs.missing import NAType
import plotly.graph_objects as go

from lolla.constants import STAGES, HOURS
from lolla.artists import Artist, ArtistSize, Genre


def display_schedule(schedule_df: pd.DataFrame) -> None:
    """Display the schedule using a Plotly figure."""
    fig = get_schedule_plotly_figure(schedule_df)
    fig.show()


def get_schedule_plotly_figure(schedule_df: pd.DataFrame) -> go.Figure:
    display_df = schedule_df.copy()
    display_df.index = pd.Series(display_df.index).apply(
        lambda x: f"{x % 12 if x > 12 else x}:00"
    )

    # Convert the artist objects to a string representation
    for stage in STAGES:
        display_df[stage] = display_df[stage].apply(artist_to_display)

    # Build cell background colors by artist size
    # Transparent for empty, blue for small, yellow for medium, red for large
    color_map = {
        ArtistSize.SMALL: "rgba(0,0,255,0.2)",
        ArtistSize.MEDIUM: "rgba(255,255,102,0.2)",
        ArtistSize.LARGE: "rgba(255,0,0,0.2)",
    }
    cell_colors = []
    # index column colors (leave transparent)
    cell_colors.append(["rgba(0,0,0,0)" for _ in schedule_df.index])
    # stage columns
    for stage in STAGES:
        col_colors = []
        for hour in schedule_df.index:
            artist = schedule_df.at[hour, stage]
            if isinstance(artist, Artist):
                col_colors.append(color_map.get(artist.size, "rgba(0,0,0,0)"))
            else:
                col_colors.append("rgba(0,0,0,0)")
        cell_colors.append(col_colors)

    fig = go.Figure(
        data=[
            go.Table(
                domain=dict(x=[0, 1], y=[0, 0.77]),
                header=dict(
                    values=["Time"] + STAGES,
                    fill_color="lightgrey",
                    align="center",
                    font=dict(color="black", size=25),
                    height=40,
                ),
                cells=dict(
                    values=[display_df.index.tolist()]
                    + [display_df[col].tolist() for col in STAGES],
                    fill_color=cell_colors,
                    align="center",
                    font=dict(color="black", size=18),
                    height=50,
                ),
            )
        ]
    )

    # Set the layout
    fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=3, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return add_background_image(fig)


def add_background_image(fig: go.Figure) -> go.Figure:
    """Add a background image to the figure."""
    # Add a background image
    background_image_path = (
        Path(__file__).parent.parent / "resources" / "schedule_background.png"
    )
    with open(background_image_path, "rb") as f:
        img_bytes = f.read()
    img_b64 = base64.b64encode(img_bytes).decode()

    return fig.add_layout_image(
        dict(
            source="data:image/png;base64," + img_b64,
            xref="paper",
            yref="paper",
            x=0,
            y=1,  # position top-left corner
            sizex=1,
            sizey=1,  # span full width & height
            sizing="stretch",  # stretch to fill
            layer="below",  # render beneath the table
        )
    )


def artist_to_display(artist: Artist | NAType) -> str:
    if pd.isna(artist):
        return ""

    ICONS = {
        Genre.INDIE: "🎸",
        Genre.POP: "🎤",
        Genre.EDM: "🎛🔊️",
        Genre.RAP: "🔥",
    }

    return f"{ICONS[artist.genre]} {artist.name}<br>{artist.size.name.title()}<br>{artist.genre.name.title()}"


def read_schedule_from_csv(file_path: str) -> pd.DataFrame:
    """Read a schedule from a CSV file."""
    schedule_df = pd.read_csv(file_path)
    for col in schedule_df.columns:
        schedule_df[col] = schedule_df[col].apply(Artist.from_str)

    schedule_df.index = HOURS
    return schedule_df


if __name__ == "__main__":
    schedule_path = Path(__file__).parent.parent / "schedules" / "schedule.csv"
    schedule_df = read_schedule_from_csv(schedule_path)
    display_schedule(schedule_df)
