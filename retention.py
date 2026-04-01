from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plots


# create app instance
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# define the layout
app.layout = dbc.Container([
    html.H1("User Retention"),
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
@app.callback(
        [Output("retention_curve", "figure"),
         Output("cohort_table", "figure")],
        [Input("student_type", "value")]
)
def update_graphs(stud_type):
    curve = plots.retention_curve(stud_type)
    table = plots.cohort_table(stud_type)
    return curve, table


if __name__ == "__main__":
    app.run(debug=True)
