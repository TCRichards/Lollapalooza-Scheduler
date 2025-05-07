import base64
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

from lolla.constants import STAGES
from lolla.artists import Artist, ArtistSize


def display_schedule(schedule_df: pd.DataFrame) -> None:
    """Display the schedule using a Plotly figure."""
    fig = get_schedule_plotly_figure(schedule_df)
    fig.show()


def get_schedule_plotly_figure(schedule_df: pd.DataFrame) -> go.Figure:
    display_df = schedule_df.copy()
    display_df.index = pd.Series(display_df.index).apply(lambda x: f"{x % 12 if x > 12 else x}:00")

    # Build cell background colors by artist size
    # Transparent for empty, blue for small, green for medium, red for large
    color_map = {
        ArtistSize.SMALL: "rgba(0,0,255,0.2)",
        ArtistSize.MEDIUM: "rgba(0,128,0,0.2)",
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

    display_df.index = display_df.index.astype(str)

    # For each artist, replace it in the table with artist.display_name()
    for stage in STAGES:
        display_df[stage] = display_df[stage].apply(
            lambda artist: artist.display_name() if isinstance(artist, Artist) else ""
        )

    fig = go.Figure(
        data=[
            go.Table(
                domain=dict(x=[0, 1], y=[0, 0.66]),
                header=dict(
                    values=["Time"] + STAGES,
                    fill_color="lightgrey",
                    align="center",
                    font=dict(color="black", size=20),
                ),
                cells=dict(
                    values=[display_df.index.tolist()]
                    + [display_df[col].tolist() for col in STAGES],
                    fill_color=cell_colors,
                    align="center",
                    font=dict(color="black", size=16),
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



if __name__ == "__main__":
    schedule_path = Path(__file__).parent.parent / "schedules" / "schedule.csv"
    schedule_df = pd.read_csv(schedule_path)
    display_schedule(schedule_df)
