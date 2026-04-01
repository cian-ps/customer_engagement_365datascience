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
register_page(__name__, path="/")

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
        ], width=4),
        dbc.Col([
            dcc.Markdown("To"),
            dcc.DatePickerSingle(
                    id="date_end",
                    min_date_allowed=min_date,
                    max_date_allowed=max_date,
                    date=max_date
                )
        ], width=4),
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
        dbc.Col([
            dcc.Graph(id="kpi_1", figure={})
        ], width=4),
        dbc.Col([
            dcc.Graph(id="kpi_2", figure={})
        ], width=4),
        dbc.Col([
            dcc.Graph(id="kpi_3", figure={})
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="course_metric",
                options=["Total", "Per Student", "Completion Rate"],
                value="Total",
                clearable=False
            )
        ], width=4),
        dbc.Col([
            dcc.Dropdown(
                id="limit",
                options=[{"label": l, "value": v} for l, v in zip(["Top 5", "Top 10", "Top 15", "All"], [5, 10, 15, 50])],
                value=10,
                clearable=False
            )
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="top_courses", figure={})
        ], width=8),
        dbc.Col([
            dcc.Graph(id="donut_plot", figure={})
        ], width=4)
    ])
])

# define callbacks
@callback(
        [Output("kpi_1", "figure"),
         Output("kpi_2", "figure"),
         Output("kpi_3", "figure")],
        [Input("date_start", "date"),
         Input("date_end", "date"),
         Input("student_type", "value")]
)
def update_kpis(date_start, date_end, stud_type):
    time_period = (np.datetime64(date_start), np.datetime64(date_end))
    kpi1 = plots.engagement_kpi(time_period, stud_type)
    kpi2 = plots.time_watched_kpi(time_period, stud_type)
    kpi3 = plots.certs_kpi(time_period, stud_type)
    return kpi1, kpi2, kpi3

@callback(
        [Output("top_courses", "figure"),
         Output("donut_plot", "figure")],
        [Input("course_metric", "value"),
         Input("limit", "value")]
)
def update_graphs(metric, n):
    fig_courses = plots.courses_plot(metric, n)
    fig_ratings = plots.ratings_plot()
    return fig_courses, fig_ratings
