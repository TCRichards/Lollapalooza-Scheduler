"""Module for visualizing the Lollapalooza schedule using a Plotly table."""

import pandas as pd
from typing import Optional

from lolla.scheduling.constants import STAGES, HOURS
from lolla.scheduling.artists import Artist, ArtistSize


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
            lambda a: "" if pd.isna(a) else a.to_table_display()  # Show full artist display with genre icons and newlines
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
                        ArtistSize.SMALL: 'rgba(227, 242, 253, 0.95)',
                        ArtistSize.MEDIUM: 'rgba(255, 243, 224, 0.95)',
                        ArtistSize.LARGE: 'rgba(255, 235, 238, 0.95)', 
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
                        ArtistSize.SMALL: 'rgba(227, 242, 253, 0.95)',
                        ArtistSize.MEDIUM: 'rgba(255, 243, 224, 0.95)',
                        ArtistSize.LARGE: 'rgba(255, 235, 238, 0.95)', 
                    }
                    bg_color = color_map.get(artist.size, 'transparent')
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


def read_schedule_from_csv(file_path: str) -> pd.DataFrame:
    """Read a schedule from a CSV file."""
    schedule_df = pd.read_csv(file_path)
    for col in schedule_df.columns:
        schedule_df[col] = schedule_df[col].apply(Artist.from_str)

    schedule_df.index = HOURS
    return schedule_df


if __name__ == "__main__":
    # Initializes the dash app using
    from lolla.app.app import create_app
    app = create_app()
    app.run(debug=True)
