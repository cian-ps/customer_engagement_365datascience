from dash import dcc, Input, Output, register_page, callback
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import os
import sys
from pathlib import Path


# import plotting functions
base_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent
sys.path.append(str(base_dir))
import plots

# register page
register_page(__name__, path="/engagement")

# set min/max dates
df = pd.read_csv("data/engagement.csv")
df.engagement_date = pd.to_datetime(df.engagement_date)
min_date = df.engagement_date.min()
max_date = df.engagement_date.max()

# define the layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Markdown("From"),
            dcc.DatePickerSingle(
                    id="date_start",
                    min_date_allowed=min_date,
                    max_date_allowed=max_date,
                    date=min_date
                )
        ], width=6),
        dbc.Col([
            dcc.Markdown("To"),
            dcc.DatePickerSingle(
                    id="date_end",
                    min_date_allowed=min_date,
                    max_date_allowed=max_date,
                    date=max_date
                )
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Markdown("Student Type"),
            dcc.Dropdown(
                id="student_type",
                value="All",
                options=["All", "Free", "Paid"],
                clearable=False
            )
        ], width=6),
        dbc.Col([
            dcc.Markdown("View"),
            dcc.Dropdown(
                id="view",
                options=["Daily", "Monthly"],
                value="Daily",
                clearable=False
            )
        ], width=6)
    ]),
    dbc.Row([
        dcc.Graph(id="engagement_plot", figure={})
    ]),
    dbc.Row([
        dcc.Graph(id="onboarding_plot", figure={})
    ])
])

# define callbacks
@callback(
        [Output("engagement_plot", "figure"),
         Output("onboarding_plot", "figure")],
        [Input("date_start", "date"),
         Input("date_end", "date"),
         Input("student_type", "value"),
         Input("view", "value")]
)
def update_graphs(date_start, date_end, stud_type, view):
    date_range = (np.datetime64(date_start), np.datetime64(date_end))
    fig_engage = plots.engagement_plot(view, stud_type, date_range)
    fig_onboard = plots.onboarding_plot(view, date_range)
    return fig_engage, fig_onboard
