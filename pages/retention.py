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
register_page(__name__, path="/retention")

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
        dcc.Graph(id="retention_curve", figure={})
    ]),
    dbc.Row([
        dcc.Graph(id="cohort_table", figure={})
    ])
])

# define callbacks
@callback(
        [Output("retention_curve", "figure"),
         Output("cohort_table", "figure")],
        [Input("student_type", "value")]
)
def update_graphs(stud_type):
    curve = plots.retention_curve(stud_type)
    table = plots.cohort_table(stud_type)
    return curve, table
