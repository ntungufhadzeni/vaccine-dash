from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from flask_login import login_user
from werkzeug.security import check_password_hash
from app import app
from models import Users

layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H4('Welcome to HPV Monitor Dashboard', style={'text-align': 'center', 'margin-top': '80px'})
        )
    ),
    dbc.Row(
        dbc.Col([
            html.Img(
                src='assets/logo.png',
                className='center',
                height=250
            )
        ],width={"size": 6, "offset": 5},
        )
    ),
    html.Br(),
    dbc.Row(
        dbc.Col(
            [
                dbc.Label("Email", className="mr-2"),
                dbc.Input(
                    type='text',
                    id='email',
                    className='form-control',
                    n_submit=0
                )
            ],
            width={"size": 6, "offset": 3},
        )
    ),
    dbc.Row(
        dbc.Col(
            [
                dbc.Label("Password", className="mr-2"),
                dbc.Input(
                    type='password',
                    id='password',
                    className='form-control',
                    n_submit=0,
                )
            ],
            width={"size": 6, "offset": 3},
        )
    ),
    dbc.Row(
        dbc.Col(
            dcc.Checklist(id='remember', className="mr-2",
                          options=[{"label": 'Remember me', "value": "remember"}]
                          ),
            width={"size": 3, "offset": 3},
        ),
    ),
    dbc.Row(
        dbc.Col(
            dbc.Button("Login", id="login-btn", color="dark", n_clicks=0),
            width={"size": 3, "offset": 3},
        ),
    ),
    dbc.Row(
        dbc.Col(
            [
                dcc.Location(id='url-login', pathname='/', refresh=True),
                dcc.Store(id="is-authenticated", data=False)
            ],
            width={"size": 6, "offset": 3},
        ),
        className="mt-3"
    )
])


@app.callback(Output('url-login', 'pathname'),
              Input('login-btn', 'n_clicks'),
              [State('email', 'value'),
               State('password', 'value'),
               State('remember', 'value')])
def login_page(n_clicks, email, password, remember):
    if n_clicks > 0:
        user = Users.query.filter_by(email=email).first()
        if user:
            remember = True if remember else False
            if check_password_hash(user.encrypted_password, password):
                login_user(user, remember=remember)
                return '/dashboard'
            else:
                pass
        else:
            pass
    else:
        pass


@app.callback(Output('username', 'className'),
              [Input('login-btn', 'n_clicks'),
               Input('email', 'n_submit')],
              [State('email', 'value')])
def update_username_output(n_clicks, n_submit, email):
    if n_clicks > 0 or n_submit > 0:
        user = Users.query.filter_by(email=email).first()
        if user:
            return 'form-control'
        else:
            return 'form-control is-invalid'
    else:
        return 'form-control'


@app.callback(Output('password', 'className'),
              [Input('login-btn', 'n_clicks'),
               Input('email', 'n_submit'),
               Input('password', 'n_submit')],
              [State('email', 'value'),
               State('password', 'value')])
def update_password_output(n_clicks, username_submit, password_submit, email, password):
    if n_clicks > 0 or username_submit > 0 or password_submit > 0:
        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.encrypted_password, password):
                return 'form-control'
            else:
                return 'form-control is-invalid'
        else:
            return 'form-control'
    return 'form-control'

