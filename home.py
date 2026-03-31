from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plots

# create app instance
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# set min/max dates
df = pd.read_csv("data/engagement.csv")
df.engagement_date = pd.to_datetime(df.engagement_date)
min_date = df.engagement_date.min()
max_date = df.engagement_date.max()

# define page layout
app.layout = dbc.Container([
    html.H1("Overview"),
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
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Markdown("Student Type"),
            dcc.Dropdown(
                    id="student_type",
                    value="All",
                    options=["All", "Free", "Paid"]
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
    ])
])

# define callbacks
@app.callback(
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

if __name__ == "__main__":
    app.run(debug=True)