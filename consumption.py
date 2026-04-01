from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plots


# create app instance
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# define the layout
app.layout = dbc.Container([
    html.H1("Content Consumption"),
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
@app.callback(
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


if __name__ == "__main__":
    app.run(debug=True)
