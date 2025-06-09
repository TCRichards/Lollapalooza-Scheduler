"""Module for visualizing the Lollapalooza schedule using a Plotly table."""

import base64
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from typing import Optional
from dash import dash_table, html
from lolla.constants import STAGES, HOURS
from lolla.artists import Artist, ArtistSize


def get_schedule_datatable_data(schedule_df: pd.DataFrame, highlight_row: Optional[int] = None) -> tuple[list[dict], list[dict], list[dict]]:
    """Get data, columns, and style_data_conditional for the schedule DataTable."""
    # Prepare the data for DataTable
    display_df = schedule_df.copy()
    
    # Convert time index to readable format
    display_df.index = pd.Series(display_df.index).apply(
        lambda x: f"{x % 12 if x > 12 else x}:00"
    )
    
    # Convert artists to display format
    for stage in STAGES:
        display_df[stage] = display_df[stage].apply(
            lambda a: "" if pd.isna(a) else a.name  # Just show artist name for cleaner table
        )
    
    # Reset index to make Time a regular column
    display_df = display_df.reset_index()
    display_df = display_df.rename(columns={'index': 'Time'})
    
    # Define color mapping for conditional formatting
    def get_cell_style(schedule_df, row_idx, col_name):
        """Get the background color for a cell based on artist size."""
        if col_name == 'Time':
            return 'background-color: lightgrey; font-weight: bold; text-align: center;'
        
        original_row_idx = row_idx  # Since we reset index
        if original_row_idx < len(schedule_df):
            artist = schedule_df.iloc[original_row_idx][col_name]
            if isinstance(artist, Artist):
                color_map = {
                    ArtistSize.SMALL: '#e3f2fd',  # Light blue
                    ArtistSize.MEDIUM: '#fff3e0',  # Light orange
                    ArtistSize.LARGE: '#ffebee',   # Light red
                }
                bg_color = color_map.get(artist.size, 'white')
                return f'background-color: {bg_color}; text-align: center; cursor: pointer;'
        return 'background-color: white; text-align: center; cursor: pointer;'
    
    # Create conditional formatting rules
    style_data_conditional = []
    
    # Highlight the current hour row
    if highlight_row is not None and 0 <= highlight_row < len(display_df):
        style_data_conditional.append({
            'if': {'row_index': highlight_row},
            'backgroundColor': '#c8e6c9',  # Light green for highlighted row
            'fontWeight': 'bold'
        })
    
    # Add artist size-based coloring
    for row_idx in range(len(display_df)):
        for col_name in STAGES:
            if row_idx < len(schedule_df):
                artist = schedule_df.iloc[row_idx][col_name]
                if isinstance(artist, Artist):
                    color_map = {
                        ArtistSize.SMALL: '#e3f2fd',  # Light blue
                        ArtistSize.MEDIUM: '#fff3e0',  # Light orange  
                        ArtistSize.LARGE: '#ffebee',   # Light red
                    }
                    bg_color = color_map.get(artist.size, 'white')
                    style_data_conditional.append({
                        'if': {
                            'row_index': row_idx,
                            'column_id': col_name
                        },
                        'backgroundColor': bg_color,
                        'cursor': 'pointer'
                    })
    
    # Return data, columns, and style_data_conditional for use in callback
    columns = [
        {'name': 'Time', 'id': 'Time', 'type': 'text'},
        *[{'name': stage, 'id': stage, 'type': 'text'} for stage in STAGES]
    ]
    
    data = display_df.to_dict('records')
    
    return data, columns, style_data_conditional


def get_schedule_datatable(schedule_df: pd.DataFrame, highlight_row: Optional[int] = None) -> html.Div:
    """Create a complete DataTable component wrapped in a Div (for standalone use)."""
    data, columns, style_data_conditional = get_schedule_datatable_data(schedule_df, highlight_row)
    
    datatable = dash_table.DataTable(
        id='schedule-table-standalone',
        data=data,
        columns=columns,
        style_table={
            'height': '80vh',
            'overflowY': 'auto',
            'border': '2px solid #e74c3c',
            'borderRadius': '10px'
        },
        style_header={
            'backgroundColor': '#e74c3c',
            'color': 'white',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'fontSize': '18px',
            'padding': '12px'
        },
        style_cell={
            'textAlign': 'center',
            'padding': '15px',
            'fontSize': '14px',
            'fontFamily': 'Arial, sans-serif',
            'border': '1px solid #ddd',
            'minWidth': '120px',
            'maxWidth': '200px',
            'whiteSpace': 'normal',
            'height': '30px',
        },
        style_data={
            'backgroundColor': 'white',
            'color': 'black',
        },
        style_data_conditional=style_data_conditional,
        # Enable cell clicking
        cell_selectable=False,  # Disable cell selection highlighting
        row_selectable=False,   # Disable row selection
        # Enable active cell for click detection
        active_cell=None,  # This enables the active_cell property for callbacks
    )
    
    return html.Div([
        html.H3("🎪 Lollapalooza Schedule", 
                style={'textAlign': 'center', 'color': '#e74c3c', 'marginBottom': '20px'}),
        html.P("Click on any artist to watch their video!", 
               style={'textAlign': 'center', 'color': '#666', 'marginBottom': '20px'}),
        datatable
    ], style={'padding': '20px'})


def read_schedule_from_csv(file_path: str) -> pd.DataFrame:
    """Read a schedule from a CSV file."""
    schedule_df = pd.read_csv(file_path)
    for col in schedule_df.columns:
        schedule_df[col] = schedule_df[col].apply(Artist.from_str)

    schedule_df.index = HOURS
    return schedule_df


def get_schedule_plotly_figure(schedule_df: pd.DataFrame, highlight_row: Optional[int] = None) -> go.Figure:
    """Create a Plotly table figure for the schedule (for backward compatibility)."""
    
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

    # Highlight the index (hour) based on whether it's the active hour
    cell_colors = []
    cell_colors.append([
        highlight_color if i == highlight_row else base_color
        for i in range(len(schedule_df))
    ])

    for stage in STAGES:
        col_colors = []
        for hour in schedule_df.index:
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
                    line=dict(color="white", width=2),
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


if __name__ == "__main__":
    # Initializes the dash app using 
    from lolla.app import create_app
    app = create_app()
    app.run(debug=True)
