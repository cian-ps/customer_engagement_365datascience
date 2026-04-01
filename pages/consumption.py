from dash import dcc, Input, Output, register_page, callback
import dash_bootstrap_components as dbc
import os
import sys
from pathlib import Path


# import plotting functions
base_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent
sys.path.append(str(base_dir))
import plots

# register page
register_page(__name__, path="/consumption")

# define the layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Markdown("Student Type"),
            dcc.Dropdown(
                id="student_type",
                value="All",
                options=["All", "Free", "Paid"],
                clearable=False
            )
        ], width=4)
    ]),
    dbc.Row([
        dcc.Graph(id="total_consumption", figure={})
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="subscription_rate", figure={})
        ], width=6),
        dbc.Col([
            dcc.Graph(id="subscription_duration", figure={})
        ], width=6)
    ])
])

# define callbacks
@callback(
        [Output("total_consumption", "figure"),
         Output("subscription_rate", "figure"),
         Output("subscription_duration", "figure")],
        [Input("student_type", "value")]
)
def update_graphs(stud_type):
    fig_consume = plots.consumption_plot(stud_type)
    fig_f2p = plots.sub_rate_plot()
    fig_duration = plots.sub_duration_plot()
    return fig_consume, fig_f2p, fig_duration
