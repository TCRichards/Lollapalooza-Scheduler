"""A Dash app that generates a Lolalapoo schedule and visualizes it in a table format."""

import dash
from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

from lolla.generate_schedule import generate_valid_schedule
from lolla.visualize import generate_table
from lolla.youtube import get_youtube_video_id, create_youtube_embed


def create_app(schedule_df: pd.DataFrame) -> dash.Dash:
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = html.Div([
        dcc.Graph(id="schedule-graph", figure=generate_table(schedule_df), style={"height": "100vh"}),
        html.Div(id="video-player", style={"textAlign": "center", "margin": "20px"}),
        dbc.Row([
            dbc.Col(dbc.Button("⬅️ Previous", id="prev-btn", n_clicks=0, color="primary")),
            dbc.Col(dbc.Button("➡️ Next Hour", id="next-btn", n_clicks=0, color="success")),
        ], justify="center", className="mt-2"),
        dcc.Store(id="highlight-index", data=-1),
        dcc.Store(id="video-index", data=0),
        dbc.Row([
            dbc.Col(dbc.Button("⬅️ Prev Song", id="prev-song", n_clicks=0, color="secondary")),
            dbc.Col(dbc.Button("➡️ Next Song", id="next-song", n_clicks=0, color="secondary")),
        ], justify="center", className="mt-2"),
        dbc.Row([
            dbc.Col(dbc.Button("▶️ Play Song", id="play-song", n_clicks=0, color="danger")),
        ], justify="center", className="mt-2"),
        dcc.Store(id="play-trigger", data=False),
    ])

    @app.callback(
        Output("highlight-index", "data"),
        Input("prev-btn", "n_clicks"),
        Input("next-btn", "n_clicks"),
        State("highlight-index", "data")
    )
    def update_index(prev_clicks, next_clicks, current_idx):
        changed_id = dash.callback_context.triggered_id
        if changed_id == "prev-btn":
            return max(current_idx - 1, 0)
        elif changed_id == "next-btn":
            return min(current_idx + 1, len(schedule_df) - 1)
        return current_idx

    @app.callback(
        Output("video-index", "data"),
        Input("prev-song", "n_clicks"),
        Input("next-song", "n_clicks"),
        State("video-index", "data"),
        State("highlight-index", "data"),
    )
    def update_video_index(prev_clicks, next_clicks, current_video_idx, current_hour_idx):
        if current_hour_idx is None or current_hour_idx < 0 or current_hour_idx >= len(schedule_df):
            return 0
        this_hour_artists = schedule_df.iloc[current_hour_idx].dropna()
        total_artists = len(this_hour_artists)
        triggered_id = dash.callback_context.triggered_id
        if triggered_id == "prev-song":
            return max(current_video_idx - 1, 0)
        elif triggered_id == "next-song":
            return min(current_video_idx + 1, total_artists - 1)
        return current_video_idx

    @app.callback(
        Output("play-trigger", "data"),
        Input("play-song", "n_clicks"),
        prevent_initial_call=True
    )
    def trigger_play(n_clicks):
        return True

    @app.callback(
        Output("schedule-graph", "figure"),
        Input("highlight-index", "data")
    )
    def update_figure(current_idx):
        return generate_table(schedule_df, highlight_row=current_idx)

    @app.callback(
        Output("video-player", "children"),
        Input("highlight-index", "data"),
        Input("video-index", "data"),
        Input("play-trigger", "data")
    )
    def update_video_embed(current_idx, video_idx, play_trigger):
        if not play_trigger:
            return html.Div("Press ▶️ to play a song.")
        if current_idx is None or current_idx < 0 or current_idx >= len(schedule_df):
            return html.Div("Select an hour to see videos.")
        this_hour_artists = schedule_df.iloc[current_idx].dropna()
        artist_names = [artist.name for artist in this_hour_artists]
        if not artist_names or video_idx >= len(artist_names):
            return html.Div("No video available.")
        video_id = get_youtube_video_id(artist_names[video_idx])
        return create_youtube_embed(video_id)

    return app


def main():
    # Generates a valid schedule and creates the Dash app
    schedule_df = generate_valid_schedule()
    app = create_app(schedule_df)
    app.run(debug=True)


if __name__ == "__main__":
    main()
