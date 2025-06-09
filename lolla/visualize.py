"""Module for visualizing the Lollapalooza schedule using a Plotly table."""

import base64
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from typing import Optional
from lolla.constants import STAGES, HOURS
from lolla.artists import Artist, ArtistSize



def get_schedule_plotly_figure(schedule_df: pd.DataFrame, highlight_row: Optional[int] = None) -> go.Figure:
    display_df = schedule_df.copy()
    display_df.index = pd.Series(display_df.index).apply(
        lambda x: f"{x % 12 if x > 12 else x}:00"
    )

    for stage in STAGES:
        display_df[stage] = display_df[stage].apply(lambda a: "" if pd.isna(a) else a.to_display())

    color_map = {
        ArtistSize.SMALL: "rgba(0,0,255,0.2)",
        ArtistSize.MEDIUM: "rgba(255,255,102,0.2)",
        ArtistSize.LARGE: "rgba(255,0,0,0.2)",
    }
    base_color = "rgba(0,0,0,0)"
    highlight_color = "rgba(0,255,0,0.4)"

    # Highlight the index (hour) vased on whether it's the active hour
    cell_colors = []
    cell_colors.append([
        highlight_color if i == highlight_row else base_color
        for i in range(len(schedule_df))
    ])

    for stage in STAGES:
        col_colors = []
        for  hour in schedule_df.index:
            artist = schedule_df.at[hour, stage]
            bg_color = color_map.get(artist.size, base_color) if isinstance(artist, Artist) else base_color
            col_colors.append(bg_color)
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
                    values=[display_df.index.tolist()] +
                           [display_df[col].tolist() for col in STAGES],
                    fill_color=cell_colors,
                    align="center",
                    font=dict(color="black", size=18),
                    height=50,
                ),
            )
        ]
    )
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


def read_schedule_from_csv(file_path: str) -> pd.DataFrame:
    """Read a schedule from a CSV file."""
    schedule_df = pd.read_csv(file_path)
    for col in schedule_df.columns:
        schedule_df[col] = schedule_df[col].apply(Artist.from_str)

    schedule_df.index = HOURS
    return schedule_df


if __name__ == "__main__":
    # Initializes the dash app using 
    schedule_path = Path(__file__).parent.parent / "schedules" / "schedule.csv"
    schedule_df = read_schedule_from_csv(schedule_path)

    from lolla.app import create_app
    app = create_app(schedule_df)
    app.run(debug=True)
