"""A Dash app that generates a fake Lolalapooza schedule lineup and visualizes it in a table format."""

import dash
from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
from dash_extensions import EventListener
import pandas as pd

from lolla.constants import STAGES 
from lolla.artists import Artist
from lolla.visualize import get_schedule_plotly_figure
from lolla.youtube import get_youtube_video_id, create_youtube_embed
from lolla.generate_schedule import generate_valid_schedule


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
    from lolla.constants import HOURS
    
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
    schedule_df.index = HOURS[:len(schedule_df)]
    return schedule_df


def create_app() -> dash.Dash:
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = html.Div(
        [
            # Landing page components
            html.Div(
                id="landing-page",
                children=[
                    dbc.Container(
                        [
                            dbc.Row(
                                dbc.Col(
                                    [
                                        html.H1(
                                            "🎵 Lollapalooza Schedule Generator",
                                            className="text-center mb-4",
                                            style={"color": "#e74c3c", "fontWeight": "bold"}
                                        ),
                                        html.P(
                                            "Welcome! Click the button below to generate a custom Lollapalooza festival schedule.",
                                            className="text-center lead mb-4",
                                        ),
                                        dbc.Button(
                                            "🎪 Generate Schedule",
                                            id="start-btn",
                                            n_clicks=0,
                                            color="primary",
                                            size="lg",
                                            className="d-block mx-auto",
                                        ),
                                    ],
                                    width=8,
                                ),
                                justify="center",
                            )
                        ],
                        className="mt-5",
                    )
                ],
                style={"minHeight": "100vh", "backgroundColor": "#f8f9fa"},
            ),
            # Schedule viewer components (initially hidden)
            html.Div(
                id="schedule-viewer",
                children=[
                    EventListener(
                        dcc.Graph(
                            id="schedule-graph",
                            style={"height": "100vh"},
                        ),
                        events=[{"event": "click", "props": ["x", "y"]}],
                        id="graph-listener",
                        logging=True,
                    ),
                    html.Div(
                        id="video-player", style={"textAlign": "center", "margin": "20px"}
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Button(
                                    "⬅️ Previous Hour",
                                    id="prev-btn",
                                    n_clicks=0,
                                    color="primary",
                                )
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "➡️ Next Hour", 
                                    id="next-btn", 
                                    n_clicks=0, 
                                    color="success"
                                )
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "🔄 Generate New Schedule",
                                    id="regenerate-btn",
                                    n_clicks=0,
                                    color="warning",
                                )
                            ),
                        ],
                        justify="center",
                        className="mt-2",
                    ),
                ],
                style={"display": "none"},
            ),
            # Data stores
            dcc.Store(id="highlight-index", data=-1),
            dcc.Store(id="video-index", data=0),
            dcc.Store(id="schedule-data", data=None),
            dcc.Store(id="app-state", data="landing"),  # "landing" or "schedule"
        ]
    )

    @app.callback(
        [
            Output("schedule-data", "data"),
            Output("app-state", "data"),
            Output("landing-page", "style"),
            Output("schedule-viewer", "style"),
        ],
        [
            Input("start-btn", "n_clicks"),
            Input("regenerate-btn", "n_clicks"),
        ],
        prevent_initial_call=True,
    )
    def handle_schedule_generation(start_clicks, regenerate_clicks):
        """Generate schedule and switch to schedule view."""
        if start_clicks > 0 or regenerate_clicks > 0:
            schedule_df = generate_valid_schedule()
            # Convert DataFrame to dictionary for storage
            schedule_data = serialize_schedule_df(schedule_df)
            return (
                schedule_data,
                "schedule", 
                {"display": "none"},  # hide landing page
                {"display": "block"}  # show schedule viewer
            )
        return dash.no_update

    @app.callback(
        Output("highlight-index", "data"),
        [
            Input("prev-btn", "n_clicks"),
            Input("next-btn", "n_clicks"),
        ],
        [
            State("highlight-index", "data"),
            State("schedule-data", "data"),
        ],
    )
    def update_index(prev_clicks, next_clicks, current_idx, schedule_data):
        if not schedule_data:
            return current_idx
            
        schedule_df = deserialize_schedule_df(schedule_data)
        changed_id = dash.callback_context.triggered_id
        if changed_id == "prev-btn":
            return max(current_idx - 1, 0)
        elif changed_id == "next-btn":
            return min(current_idx + 1, len(schedule_df) - 1)
        return current_idx

    @app.callback(
        Output("schedule-graph", "figure"),
        [
            Input("schedule-data", "data"),
            Input("highlight-index", "data"),
        ],
    )
    def update_schedule_graph(schedule_data, current_idx):
        if not schedule_data:
            return {}
            
        schedule_df = deserialize_schedule_df(schedule_data)
        return get_schedule_plotly_figure(schedule_df, highlight_row=current_idx)

    @app.callback(
        Output("video-player", "children"),
        Input("graph-listener", "n_events"),
        State("schedule-data", "data"),
    )
    def play_video_on_click(event, schedule_data):
        if not event or "points" not in event or not event["points"]:
            return dash.no_update

        point = event["points"][0]
        row = point["pointIndex"]
        col = point["curveNumber"]  # 0 = time, 1+ = stages

        if col == 0:
            return dash.no_update  # they clicked the time index

        schedule_df = deserialize_schedule_df(schedule_data)
        stage = STAGES[col - 1]
        artist = schedule_df.iloc[row][stage]
        if not isinstance(artist, Artist):
            return html.Div("No artist scheduled in this slot.")

        video_id = get_youtube_video_id(artist.name)
        return create_youtube_embed(video_id)

    return app


def main():
    app = create_app()
    app.run(debug=True)


if __name__ == "__main__":
    main()
