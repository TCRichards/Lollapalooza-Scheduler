import dash
from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

from lolla.generate_schedule import generate_valid_schedule
from lolla.visualize import generate_table


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
schedule_df = generate_valid_schedule()

app.layout = html.Div([
    dcc.Graph(id="schedule-graph", figure=generate_table(schedule_df), style={"height": "100vh"}),
    dbc.Row([
        dbc.Col(dbc.Button("⬅️ Previous", id="prev-btn", n_clicks=0, color="primary")),
        dbc.Col(dbc.Button("➡️ Next", id="next-btn", n_clicks=0, color="success")),
    ], justify="center", className="mt-2"),
    dcc.Store(id="highlight-index", data=-1)
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
    Output("schedule-graph", "figure"),
    Input("highlight-index", "data")
)
def update_figure(current_idx):
    return generate_table(schedule_df, highlight_row=current_idx)

app.run(debug=True)