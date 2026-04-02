from dash import Dash, html, page_container
import dash_bootstrap_components as dbc


# create the app instance
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LUX])
server = app.server

# create navbar
navbar = dbc.NavbarSimple(
    [dbc.NavItem(dbc.NavLink("Home", href="/")),
    dbc.NavItem(dbc.NavLink("Engagament", href="/engagement")),
    dbc.NavItem(dbc.NavLink("Retention", href="/retention")),
    dbc.NavItem(dbc.NavLink("Consumption", href="/consumption")),
    dbc.NavItem(dbc.NavLink("Exams", href="/exams"))],
    brand="Customer Engagement Dashboard",
    brand_href="/",
    color="dark",
    dark=True
)

# define the layout
app.layout = html.Div([
    navbar,
    page_container
])

# run the app
if __name__ == "__main__":
    app.run(debug=True)
