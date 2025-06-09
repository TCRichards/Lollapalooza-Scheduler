"""Alternative visualization using clickable scatter plot to mimic table."""

import base64
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Optional
from lolla.scheduling.constants import STAGES, HOURS
from lolla.scheduling.artists import Artist, ArtistSize
import numpy as np


def get_schedule_plotly_figure_clickable(schedule_df: pd.DataFrame, highlight_row: Optional[int] = None) -> go.Figure:
    """Create a clickable version of the schedule using scatter plot."""
    
    # Create a grid of x,y coordinates for each cell
    fig = go.Figure()
    
    # Add invisible scatter points for each cell to enable clicking
    for stage_idx, stage in enumerate(STAGES):
        for hour_idx, hour in enumerate(schedule_df.index):
            artist = schedule_df.at[hour, stage]
            
            # Color based on artist size
            if isinstance(artist, Artist):
                if artist.size == ArtistSize.SMALL:
                    color = "rgba(0,0,255,0.7)"
                elif artist.size == ArtistSize.MEDIUM:
                    color = "rgba(255,255,102,0.7)"
                else:  # LARGE
                    color = "rgba(255,0,0,0.7)"
                text = artist.to_display()
            else:
                color = "rgba(200,200,200,0.3)"
                text = ""
            
            # Highlight if this is the current hour
            if hour_idx == highlight_row:
                color = "rgba(0,255,0,0.6)"
            
            fig.add_trace(go.Scatter(
                x=[stage_idx],
                y=[hour_idx],
                mode='markers+text',
                marker=dict(
                    size=80,
                    color=color,
                    symbol='square',
                    line=dict(color='white', width=2)
                ),
                text=text,
                textposition="middle center",
                textfont=dict(size=10, color='black'),
                showlegend=False,
                hovertemplate=f"<b>{stage}</b><br>%{{text}}<extra></extra>",
                customdata=[[hour_idx, stage_idx + 1]]  # Store row, col for callback
            ))
    
    # Add time labels on the left
    for hour_idx, hour in enumerate(schedule_df.index):
        time_display = f"{hour % 12 if hour > 12 else hour}:00"
        fig.add_trace(go.Scatter(
            x=[-0.5],
            y=[hour_idx],
            mode='text',
            text=time_display,
            textposition="middle center",
            textfont=dict(size=14, color='black', family='Arial Black'),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Add stage headers at the top
    for stage_idx, stage in enumerate(STAGES):
        fig.add_trace(go.Scatter(
            x=[stage_idx],
            y=[len(schedule_df)],
            mode='text',
            text=stage,
            textposition="middle center",
            textfont=dict(size=16, color='black', family='Arial Black'),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Update layout to look like a table
    fig.update_layout(
        xaxis=dict(
            range=[-1, len(STAGES)],
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            fixedrange=True
        ),
        yaxis=dict(
            range=[-0.5, len(schedule_df) + 0.5],
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            autorange='reversed',  # Reverse so first hour is at top
            fixedrange=True
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=20, t=50, b=20),
        height=600,
        showlegend=False
    )
    
    return add_background_image(fig)


def add_background_image(fig: go.Figure) -> go.Figure:
    """Add a background image to the figure."""
    background_image_path = (
        Path(__file__).parent.parent / "resources" / "schedule_background.png"
    )
    
    if background_image_path.exists():
        with open(background_image_path, "rb") as f:
            img_bytes = f.read()
        img_b64 = base64.b64encode(img_bytes).decode()

        fig.add_layout_image(
            dict(
                source="data:image/png;base64," + img_b64,
                xref="paper",
                yref="paper",
                x=0,
                y=1,
                sizex=1,
                sizey=1,
                sizing="stretch",
                layer="below",
            )
        )
    
    return fig
