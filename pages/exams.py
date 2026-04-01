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
register_page(__name__, path="/exams")

# define the layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Markdown("Exam Category"),
            dcc.Dropdown(
                id="exam_category",
                options=["All", "Practice", "Course", "Career Track"],
                value="All",
                clearable=False
            )
        ], width=4)
    ]),
    dbc.Row([
        dcc.Graph(id="exams_plot", figure={})
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Markdown("Certificate Category"),
            dcc.Dropdown(
                id="cert_category",
                options=["All", "Course", "Career Track"],
                value="All",
                clearable=False
            ),
            dcc.Graph(id="certs_plot", figure={})
        ]),
        dbc.Col([
            dcc.Markdown("Select Career Track"),
            dcc.Dropdown(
                id="career_track",
                options=["Data Scientist", "Data Analyst", "Business Analyst"],
                value="Data Scientist",
                clearable=False
            ),
            dcc.Graph(id="career_track_funnel", figure={})
        ])
    ])
])

# define callbacks
@callback(
        [Output("exams_plot", "figure"),
         Output("certs_plot", "figure"),
         Output("career_track_funnel", "figure")],
        [Input("exam_category", "value"),
         Input("cert_category", "value"),
         Input("career_track", "value")]
)
def update_graphs(exam_cat, cert_cat, track):
    bar_exam = plots.exams_bar_plot(exam_cat)
    bar_cert = plots.certs_bar_plot(cert_cat)
    funnel = plots.career_track_funnel(track)
    return bar_exam, bar_cert, funnel
