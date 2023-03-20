from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from flask_login import current_user, logout_user
from app import app
from views import main_view

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(html.Div([html.Img(src="assets/logo.png", height="30px")],
                             style={'padding-right': '20px'})),
        dbc.DropdownMenu(
            id='drop-menu',
            nav=True,
            in_navbar=True,
            children=[
                dbc.DropdownMenuItem('Admin', id='index-admin', n_clicks=0),
                dbc.DropdownMenuItem('Profile', id='index-profile', n_clicks=0),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem('Logout', id='index-logout', n_clicks=0),
            ],
        )
    ],
    brand="HPV Monitor Dashboard",
    brand_href="/dashboard",
    color="primary",
    dark=True,
)

layout = html.Div(
    [
        dcc.Location(id='url-index', refresh=True),
        navbar,
        html.Br(),
        html.Div(main_view.content)
    ]
)


@app.callback(Output('url-index', 'pathname'),
              [Input('index-admin', 'n_clicks'),
               Input('index-profile', 'n_clicks'),
               Input('index-logout', 'n_clicks')])
def dashboard_link(n_clicks_admin, n_clicks_profile, n_clicks_logout):
    if n_clicks_admin > 0:
        return '/admin'
    elif n_clicks_profile > 0:
        return '/profile'
    elif n_clicks_logout > 0:
        if current_user.is_authenticated:
            logout_user()
            return '/'
        else:
            return '/'