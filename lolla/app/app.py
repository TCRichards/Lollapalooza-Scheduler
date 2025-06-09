"""A Dash app that generates a fake Lolalapooza schedule lineup and visualizes it in a table format."""

import dash
from dash import Input, Output, State, html, dcc, dash_table
import dash_bootstrap_components as dbc

from lolla.app.schedule_table import get_schedule_datatable_data
from lolla.app.youtube import get_youtube_video_id, create_youtube_embed
from lolla.app.utils import (
    serialize_schedule_df,
    deserialize_schedule_df,
    get_schedule_background_image_b64,
    get_landing_page_background_image_b64,
)
from lolla.scheduling.constants import STAGES
from lolla.scheduling.artists import Artist
from lolla.scheduling.generate_schedule import generate_valid_schedule


def create_app() -> dash.Dash:
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.config.suppress_callback_exceptions = True
    app.title = "🎪 Lollapalooza Game"

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
                                            "🎵 Lollapalooza The Game 🎵",
                                            className="text-center mb-4",
                                            style={
                                                "color": "#000000",
                                                "fontWeight": "bold",
                                            },
                                        ),
                                        html.P(
                                            "Welcome! Click the button below to generate a festival schedule and start the game.",
                                            className="text-center lead mb-4",
                                        ),
                                        dbc.Button(
                                            "🎪 Start the Game",
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
                        style={
                            "backgroundColor": "white",
                            "padding": "40px",
                            "borderRadius": "15px",
                            "boxShadow": "0 8px 32px rgba(0,0,0,0.1)",
                            "margin": "20vh auto",
                            "maxWidth": "600px",
                        },
                    )
                ],
                style={
                    "minHeight": "100vh",
                    "backgroundImage": f"url('data:image/png;base64,{get_landing_page_background_image_b64()}')",
                    "backgroundSize": "cover",
                    "backgroundPosition": "center",
                    "backgroundRepeat": "no-repeat",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                },
            ),
            # Schedule viewer components (initially hidden)
            html.Div(
                id="schedule-viewer",
                children=[
                    html.P(
                        "Click on any artist to watch their video!",
                        style={
                            "textAlign": "center",
                            "color": "#666",
                            "marginBottom": "20px",
                        },
                    ),
                    dash_table.DataTable(
                        id="schedule-table",
                        style_table={
                            "height": "90vh",
                            "width": "100%",  # Take full horizontal space
                            "overflowY": "auto",
                            "borderRadius": "10px",
                            "backgroundColor": "transparent",  # Fully transparent background
                        },
                        style_header={
                            "backgroundColor": "#000000",
                            "color": "white",
                            "fontWeight": "bold",
                            "textAlign": "center",
                            "fontSize": "18px",
                            "padding": "12px",
                            "height": "auto",
                        },
                        style_cell={
                            "textAlign": "center",
                            "padding": "12px",  # Increased padding for more vertical space
                            "fontSize": "16px",  # Slightly larger font
                            "fontFamily": "Arial, sans-serif",
                            "whiteSpace": "pre-line", # Enable line breaks for artist names
                            "height": "auto",  # Allow cells to expand vertically
                            "minHeight": "80px",  # Larger minimum height for better vertical space usage
                            "width": f"{100 / 8}vw",  # 8 columns -- take up 100% of width
                            "lineHeight": "1.4",  # Better line spacing
                        },
                        style_data={
                            "backgroundColor": "transparent",  # Fully transparent background
                            "color": "black",
                            "height": "auto",  # Allow data cells to expand
                            "fontWeight": "500",  # Slightly bolder text for better readability
                        },
                    ),
                    html.Div(
                        id="video-player",
                        style={
                            "position": "fixed",
                            "top": "0",
                            "left": "0",
                            "width": "100%",
                            "height": "100%",
                            "zIndex": "999",
                            "pointerEvents": "none",  # Allow clicks to pass through when empty
                        },
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
                                    color="success",
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
                    html.Img(
                        src=f"data:image/png;base64,{get_schedule_background_image_b64()}",
                        style={
                            "position": "absolute",
                            "top": "0",
                            "left": "0",
                            "width": "100%",
                            "height": "100%",
                            "zIndex": "-1",  # Behind all other content
                        },
                    ),
                ],
                style={
                    "display": "none",
                    "minHeight": "100vh",
                    "backgroundPosition": "center",
                    "backgroundRepeat": "no-repeat",
                    "backgroundAttachment": "fixed",
                },
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
                {"display": "block"},  # show schedule viewer
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
        [
            Output("schedule-table", "data"),
            Output("schedule-table", "columns"),
            Output("schedule-table", "style_data_conditional"),
        ],
        [
            Input("schedule-data", "data"),
            Input("highlight-index", "data"),
        ],
    )
    def update_schedule_display(schedule_data, current_idx):
        if not schedule_data:
            return [], [], []

        schedule_df = deserialize_schedule_df(schedule_data)
        data, columns, style_data_conditional = get_schedule_datatable_data(
            schedule_df, highlight_row=current_idx
        )
        return data, columns, style_data_conditional

    @app.callback(
        Output("video-player", "children"),
        Input("schedule-table", "active_cell"),
        State("schedule-data", "data"),
    )
    def play_video_on_click(active_cell, schedule_data):
        if not active_cell or not schedule_data:
            return dash.no_update

        row = active_cell["row"]
        column_id = active_cell["column_id"]

        # Ignore clicks on the Time column
        if column_id == "Time":
            return dash.no_update

        # Ensure the column is a valid stage
        if column_id not in STAGES:
            return dash.no_update

        schedule_df = deserialize_schedule_df(schedule_data)

        # Ensure we have valid indices
        if row >= len(schedule_df):
            return dash.no_update

        artist = schedule_df.iloc[row][column_id]

        if not isinstance(artist, Artist):
            return html.Div()  # Return empty div for empty slots - cleaner UX

        try:
            video_id = get_youtube_video_id(artist.name)
            if video_id:
                return html.Div(
                    [
                        # Modal-style backdrop
                        html.Div(
                            style={
                                "position": "fixed",
                                "top": "0",
                                "left": "0",
                                "width": "100%",
                                "height": "100%",
                                "backgroundColor": "rgba(0,0,0,0.7)",
                                "zIndex": "1000",
                                "display": "flex",
                                "justifyContent": "center",
                                "alignItems": "center",
                                "pointerEvents": "all",  # Enable clicks on modal
                            },
                            children=[
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H4(
                                                    f"🎵 Now Playing: {artist.name}",
                                                    style={
                                                        "margin": "0 0 10px 0",
                                                        "color": "#e74c3c",
                                                    },
                                                ),
                                                html.P(
                                                    f"{artist.size.name.title()} {artist.genre.name.title()} Artist",
                                                    style={
                                                        "margin": "0 0 15px 0",
                                                        "color": "#666",
                                                    },
                                                ),
                                                html.Div(
                                                    [
                                                        dbc.Button(
                                                            "✕ Close",
                                                            id="close-video-btn",
                                                            size="sm",
                                                            color="secondary",
                                                            style={
                                                                "marginRight": "10px"
                                                            },
                                                        ),
                                                        dbc.Button(
                                                            "🔗 Open in YouTube",
                                                            href=f"https://www.youtube.com/watch?v={video_id}",
                                                            target="_blank",
                                                            size="sm",
                                                            color="info",
                                                            external_link=True,
                                                        ),
                                                    ],
                                                    style={"marginBottom": "15px"},
                                                ),
                                            ],
                                            style={"textAlign": "center"},
                                        ),
                                        html.Div(
                                            [
                                                create_youtube_embed(
                                                    video_id, width="640", height="360"
                                                )
                                            ]
                                        ),
                                    ],
                                    style={
                                        "backgroundColor": "white",
                                        "padding": "20px",
                                        "borderRadius": "15px",
                                        "boxShadow": "0 8px 32px rgba(0,0,0,0.3)",
                                        "maxWidth": "700px",
                                        "maxHeight": "90vh",
                                        "overflow": "auto",
                                    },
                                )
                            ],
                        )
                    ]
                )
            else:
                return html.Div(
                    [
                        html.Div(
                            [
                                html.H5(
                                    f"🎵 {artist.name}",
                                    style={"color": "#e74c3c", "marginBottom": "10px"},
                                ),
                                html.P(
                                    "Sorry, no video available for this artist.",
                                    style={
                                        "color": "#666",
                                        "fontStyle": "italic",
                                        "marginBottom": "15px",
                                    },
                                ),
                                dbc.Button(
                                    "✕ Close",
                                    id="close-video-btn",
                                    size="sm",
                                    color="secondary",
                                ),
                            ],
                            style={
                                "backgroundColor": "white",
                                "padding": "30px",
                                "borderRadius": "15px",
                                "textAlign": "center",
                                "boxShadow": "0 4px 16px rgba(0,0,0,0.2)",
                                "margin": "20px auto",
                                "maxWidth": "400px",
                                "pointerEvents": "all",  # Enable clicks on error message
                            },
                        )
                    ],
                    style={
                        "position": "fixed",
                        "top": "0",
                        "left": "0",
                        "width": "100%",
                        "height": "100%",
                        "backgroundColor": "rgba(0,0,0,0.5)",
                        "zIndex": "1000",
                        "display": "flex",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "pointerEvents": "all",
                    },
                )
        except Exception:
            return html.Div(
                [
                    html.Div(
                        [
                            html.H5(
                                f"🎵 {artist.name}",
                                style={"color": "#e74c3c", "marginBottom": "10px"},
                            ),
                            html.P(
                                "Unable to load video at this time.",
                                style={
                                    "color": "#666",
                                    "fontStyle": "italic",
                                    "marginBottom": "15px",
                                },
                            ),
                            dbc.Button(
                                "✕ Close",
                                id="close-video-btn",
                                size="sm",
                                color="secondary",
                            ),
                        ],
                        style={
                            "backgroundColor": "white",
                            "padding": "30px",
                            "borderRadius": "15px",
                            "textAlign": "center",
                            "boxShadow": "0 4px 16px rgba(0,0,0,0.2)",
                            "margin": "20px auto",
                            "maxWidth": "400px",
                            "pointerEvents": "all",
                        },
                    )
                ],
                style={
                    "position": "fixed",
                    "top": "0",
                    "left": "0",
                    "width": "100%",
                    "height": "100%",
                    "backgroundColor": "rgba(0,0,0,0.5)",
                    "zIndex": "1000",
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "pointerEvents": "all",
                },
            )

    @app.callback(
        Output("video-player", "children", allow_duplicate=True),
        Input("close-video-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def close_video(n_clicks):
        if n_clicks:
            return html.Div()  # Clear the video player completely
        return dash.no_update

    return app


def main():
    app = create_app()
    app.run(debug=True)


if __name__ == "__main__":
    main()
