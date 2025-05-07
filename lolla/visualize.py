import base64
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

from lolla.constants import STAGES


def display_schedule(schedule_df: pd.DataFrame) -> None:
    """Display the schedule using a Plotly figure."""
    fig = get_schedule_plotly_figure(schedule_df)
    fig.show()


def get_schedule_plotly_figure(schedule_df: pd.DataFrame) -> go.Figure:
    """Generate a Plotly figure for the schedule."""
    # Take out nulls, and convert index to 12-hour format
    schedule_df = schedule_df.fillna("")
    schedule_df.index = pd.Series(schedule_df.index).apply(lambda x: f"{x % 12 if x > 12 else x}:00")

    # Generate the figure
    fig = go.Figure(
        data=[
            go.Table(
                domain=dict(x=[0, 1], y=[0, 0.66]),
                header=dict(
                    values=["Hour"] + STAGES,
                    fill_color="rgba(211,237,228,0.8)",
                    align="center",
                    font=dict(color="black", size=20),
                ),
                cells=dict(
                    values=[schedule_df.index.tolist()]
                    + [schedule_df[col].tolist() for col in STAGES],
                    fill_color="rgba(0,0,0,0)",
                    align="center",
                    font=dict(color="black", size=16),
                    height=50,
                ),
            )
        ]
    )

    # Add a background image
    background_image_path = (
        Path(__file__).parent.parent / "resources" / "schedule_background.png"
    )
    with open(background_image_path, "rb") as f:
        img_bytes = f.read()
    img_b64 = base64.b64encode(img_bytes).decode()
    fig.add_layout_image(
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

    # Set the layout
    fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=3, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


if __name__ == "__main__":
    schedule_path = Path(__file__).parent.parent / "schedules" / "schedule.csv"
    schedule_df = pd.read_csv(schedule_path)
    display_schedule(schedule_df)
