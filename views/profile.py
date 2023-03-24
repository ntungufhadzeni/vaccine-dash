from dash import html, dcc
import dash_bootstrap_components as dbc
from werkzeug.security import generate_password_hash, check_password_hash
from dash.dependencies import Input, Output, State
from flask_login import current_user, logout_user
from app import app, db


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(html.Div([html.Img(src="assets/logo.png", height="30px")],
                             style={'padding-right': '20px'})),
        dbc.NavItem(id='update-time'),
        dbc.DropdownMenu(
            id='drop-menu',
            nav=True,
            in_navbar=True,
            children=[
                dbc.DropdownMenuItem('Dashboard', id='profile-dash', n_clicks=0),
                dbc.DropdownMenuItem('Admin', id='profile-admin', n_clicks=0),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem('Logout', id='profile-logout', n_clicks=0),
            ],
        )
    ],
    brand="HPV Monitor Dashboard",
    brand_href="/dashboard",
    color="primary",
    dark=True,
)

layout = html.Div([
    navbar,
    dbc.Container([
        html.Br(),
        dbc.Container([
            dcc.Location(id='urlProfile', refresh=True),
            html.H3('Profile Management'),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dbc.Label('Name:'),
                    html.Br(),
                    html.Br(),
                    dbc.Label('Email:'),
                ], md=2),

                dbc.Col([
                    dbc.Label(id='profile-username', className='text-success'),
                    html.Br(),
                    html.Br(),
                    dbc.Label(id='profile-email', className='text-success'),
                ], md=4),

                dbc.Col([
                    dbc.Label('Old Password: '),
                    dcc.Input(
                        id='oldPassword',
                        type='password',
                        className='form-control',
                        placeholder='old password',
                        n_submit=0,
                        style={
                            'width': '40%'
                        },
                    ),
                    html.Br(),
                    dbc.Label('New Password: '),
                    dcc.Input(
                        id='newPassword1',
                        type='password',
                        className='form-control',
                        placeholder='new password',
                        n_submit=0,
                        style={
                            'width': '40%'
                        },
                    ),
                    html.Br(),
                    dbc.Label('Retype New Password: '),
                    dcc.Input(
                        id='newPassword2',
                        type='password',
                        className='form-control',
                        placeholder='retype new password',
                        n_submit=0,
                        style={
                            'width': '40%'
                        },
                    ),
                    html.Br(),
                    html.Button(
                        children='Update Password',
                        id='updatePasswordButton',
                        n_clicks=0,
                        type='submit',
                        className='btn btn-primary btn-lg'
                    ),
                    html.Br(),
                    html.Div(id='updateSuccess')
                ], md=6),
            ]),
        ], className='jumbotron')
    ])
])


@app.callback(
    Output('profile-username', 'children'),
    [Input('page-content', 'children')])
def currentUserName(page_content):
    try:
        username = current_user.username
        return username
    except AttributeError:
        return ''


@app.callback(
    Output('profile-email', 'children'),
    [Input('page-content', 'children')])
def currentUserEmail(page_content):
    try:
        user_email = current_user.email
        return user_email
    except AttributeError:
        return ''


@app.callback(Output('oldPassword', 'className'),
              [Input('updatePasswordButton', 'n_clicks'),
               Input('newPassword1', 'n_submit'),
               Input('newPassword2', 'n_submit')],
              [State('pageContent', 'children'),
               State('oldPassword', 'value'),
               State('newPassword1', 'value'),
               State('newPassword2', 'value')])
def validateOldPassword(n_clicks, new_password1_submit, new_password2_submit, page_content,
                        old_password, new_password1, new_password2):
    if n_clicks > 0 or new_password1_submit > 0 or new_password2_submit > 0:
        if check_password_hash(current_user.encrypted_password, old_password):
            return 'form-control is-valid'
        else:
            return 'form-control is-invalid'
    else:
        return 'form-control'


@app.callback(Output('newPassword1', 'className'),
              [Input('updatePasswordButton', 'n_clicks'),
               Input('newPassword1', 'n_submit'),
               Input('newPassword2', 'n_submit')],
              [State('newPassword1', 'value'),
               State('newPassword2', 'value')])
def validatePassword1(n_clicks, new_password1_submit, new_password2_submit, new_password1, new_password2):
    if n_clicks > 0 or new_password1_submit > 0 or new_password2_submit > 0:
        if new_password1 == new_password2:
            return 'form-control is-valid'
        else:
            return 'form-control is-invalid'
    else:
        return 'form-control'


@app.callback(Output('newPassword2', 'className'),
              [Input('updatePasswordButton', 'n_clicks'),
               Input('newPassword1', 'n_submit'),
               Input('newPassword2', 'n_submit')],
              [State('newPassword1', 'value'),
               State('newPassword2', 'value')])
def validatePassword2(n_clicks, new_password1_submit, new_password2_submit, new_password1, new_password2):
    if n_clicks > 0 or new_password1_submit > 0 or new_password2_submit > 0:
        if new_password1 == new_password2:
            return 'form-control is-valid'
        else:
            return 'form-control is-invalid'
    else:
        return 'form-control'


@app.callback(Output('updateSuccess', 'children'),
              [Input('updatePasswordButton', 'n_clicks'),
               Input('newPassword1', 'n_submit'),
               Input('newPassword2', 'n_submit')],
              [State('page-content', 'children'),
               State('oldPassword', 'value'),
               State('newPassword1', 'value'),
               State('newPassword2', 'value')])
def changePassword(n_clicks, new_password1_submit, new_password2_submit, page_content,
                   old_password, new_password1, new_password2):
    if n_clicks > 0 or new_password1_submit > 0 or new_password2_submit > 0:
        if check_password_hash(current_user.encrypted_password, old_password) and new_password1 == new_password2:
            try:
                hashed_password = generate_password_hash(new_password1, method='sha256')
                current_user.encrypted_password = hashed_password
                db.session.commit()
                return html.Div(children=['Update Successful'], className='text-success')
            except Exception as e:
                return html.Div(children=['Update Not Successful: {e}'.format(e=e)], className='text-danger')
        else:
            return html.Div(children=['Old Password Invalid'], className='text-danger')


@app.callback(Output('urlProfile', 'pathname'),
              [Input('profile-dash', 'n_clicks'),
               Input('profile-admin', 'n_clicks'),
               Input('profile-logout', 'n_clicks')])
def profile_link(n_clicks_dash, n_clicks_admin, n_clicks_logout):
    if n_clicks_dash > 0:
        return '/dashboard'
    elif n_clicks_admin > 0:
        return '/admin'
    elif n_clicks_logout > 0:
        if current_user.is_authenticated:
            logout_user()
            return '/'
        else:
            return '/'