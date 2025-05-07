from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from lolla.constants import STAGES, HOURS
from PIL import Image, ImageDraw, ImageFont


def display_schedule_plotly(schedule_df):
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=["Hour"] + STAGES, fill_color="lightblue", align="center"
                ),
                cells=dict(
                    values=[schedule_df.index.tolist()]
                    + [schedule_df[col].tolist() for col in STAGES],
                    fill_color="white",
                    align="center",
                ),
            )
        ]
    )
    fig.update_layout(
        width=900, height=600, title_text="LollaPalooza Schedule (Plotly)"
    )
    fig.show()


def display_schedule_matplotlib(schedule_df):
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axis("off")
    tbl = ax.table(
        cellText=[
            [schedule_df.loc[h, col] for col in schedule_df.columns]
            for h in schedule_df.index
        ],
        rowLabels=schedule_df.index,
        colLabels=schedule_df.columns,
        cellLoc="center",
        loc="center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.scale(1, 2)
    plt.title("LollaPalooza Schedule (Matplotlib)")
    plt.show()

def display_schedule_pil(schedule_df):
    cell_w, cell_h = 120, 40
    cols = len(STAGES) + 1
    rows = len(HOURS) + 1
    img_w, img_h = cell_w * cols, cell_h * rows
    img = Image.new("RGB", (img_w, img_h), color="white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # Draw header
    for i, text in enumerate(["Hour"] + STAGES):
        x0, y0 = i * cell_w, 0
        draw.rectangle([x0, y0, x0 + cell_w, y0 + cell_h], outline="black", fill="#D3E4CD")
        draw.text((x0 + 5, y0 + 10), str(text), font=font, fill="black")

    # Draw cells
    for r, hour in enumerate(HOURS, start=1):
        y0 = r * cell_h
        # Hour column
        draw.rectangle([0, y0, cell_w, y0 + cell_h], outline="black")
        draw.text((5, y0 + 10), str(hour), font=font, fill="black")
        # Schedule cells
        for c, stage in enumerate(STAGES, start=1):
            x0 = c * cell_w
            draw.rectangle([x0, y0, x0 + cell_w, y0 + cell_h], outline="black")
            text = schedule_df.loc[hour, stage]
            draw.text((x0 + 5, y0 + 10), text, font=font, fill="black")


if __name__ == "__main__":
    schedule_path = Path(__file__).parent.parent / "schedules" / "schedule.csv"
    schedule_df = pd.read_csv(schedule_path)
    display_schedule_plotly(schedule_df)
    display_schedule_matplotlib(schedule_df)
