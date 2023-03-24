from dash import html, dcc, exceptions
import dash_bootstrap_components as dbc
from dash import dash_table as dt
from dash.dependencies import Input, Output, State
from werkzeug.security import generate_password_hash

from app import app, db, Users
from flask_login import current_user, logout_user


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(html.Div([html.Img(src="assets/logo.png", height="30px")],
                             style={'padding-right': '20px'})),
        dbc.DropdownMenu(
            id='drop-menu',
            nav=True,
            in_navbar=True,
            children=[
                dbc.DropdownMenuItem('Dashboard', id='admin-dash', n_clicks=0),
                dbc.DropdownMenuItem('Profile', id='admin-profile', n_clicks=0),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem('Logout', id='admin-logout', n_clicks=0),
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
            dcc.Location(id='urlUserAdmin', refresh=True),
            html.H3('Add New User'),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dbc.Label('Name: '),
                    dcc.Input(
                        id='newUsername',
                        className='form-control',
                        n_submit=0,
                        style={
                            'width': '90%'
                        },
                    ),
                    html.Br(),
                    dbc.Label('Password: '),
                    dcc.Input(
                        id='newPwd1',
                        type='password',
                        className='form-control',
                        n_submit=0,
                        style={
                            'width': '90%'
                        },
                    ),
                    html.Br(),
                    dbc.Label('Retype New Password: '),
                    dcc.Input(
                        id='newPwd2',
                        type='password',
                        className='form-control',
                        n_submit=0,
                        style={
                            'width': '90%'
                        },
                    ),
                    html.Br(),
                ], md=4),

                dbc.Col([
                    dbc.Label('Email: '),
                    dcc.Input(
                        id='newEmail',
                        className='form-control',
                        n_submit=0,
                        style={
                            'width': '90%'
                        },
                    ),
                    html.Br(),
                    dbc.Label('Admin? '),
                    dcc.Dropdown(
                        id='admin',
                        style={
                            'width': '90%'
                        },
                        options=[
                            {'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0},
                        ],
                        value=0,
                        clearable=False
                    ),
                    html.Br(),
                    html.Br(),
                    html.Button(
                        children='Create User',
                        id='createUserButton',
                        n_clicks=0,
                        type='submit',
                        className='btn btn-primary btn-lg'
                    ),
                    html.Br(),
                    html.Div(id='createUserSuccess')
                ], md=4),

                dbc.Col([

                ], md=4)

            ]),
        ], className='jumbotron'),

        dbc.Container([
            html.H3('View Users'),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dt.DataTable(
                        id='users',
                        editable=True,
                        row_deletable=True,
                        columns=[{'name': 'ID', 'id': 'id'},
                                 {'name': 'Name', 'id': 'username'},
                                 {'name': 'Email', 'id': 'email'},
                                 {'name': 'Admin', 'id': 'admin'},
                                 {'deletable': True}],
                    ),
                ], md=12),
            ]),
            html.Br(),
            html.Div(id='output-users')
        ], className='jumbotron')
    ])
])


@app.callback(Output('newUsername', 'className'),
              [Input('createUserButton', 'n_clicks'),
               Input('newUsername', 'n_submit'),
               Input('newPwd1', 'n_submit'),
               Input('newPwd2', 'n_submit'),
               Input('newEmail', 'n_submit')],
              [State('newUsername', 'value')])
def validateUsername(n_clicks, username_submit, new_password1_submit,
                     new_password2_submit, new_email_submit, new_username):
    if n_clicks > 0 or username_submit > 0 or new_password1_submit > 0 or \
            new_password2_submit > 0 or new_email_submit > 0:
        if new_username is None or new_username == '':
            return 'form-control is-invalid'
        else:
            return 'form-control is-valid'
    else:
        return 'form-control'


@app.callback(Output('newPwd1', 'className'),
              [Input('createUserButton', 'n_clicks'),
               Input('newUsername', 'n_submit'),
               Input('newPwd1', 'n_submit'),
               Input('newPwd2', 'n_submit'),
               Input('newEmail', 'n_submit')],
              [State('newPwd1', 'value'),
               State('newPwd2', 'value')])
def validatePassword1(n_clicks, username_submit, new_password1_submit,
                      new_password2_submit, new_email_submit, new_password1, new_password2):
    if n_clicks > 0 or username_submit > 0 or new_password1_submit > 0 or \
            new_password2_submit > 0 or new_email_submit > 0:
        if new_password1 == new_password2 and len(new_password1) > 7:
            return 'form-control is-valid'
        else:
            return 'form-control is-invalid'
    else:
        return 'form-control'


@app.callback(Output('newPwd2', 'className'),
              [Input('createUserButton', 'n_clicks'),
               Input('newUsername', 'n_submit'),
               Input('newPwd1', 'n_submit'),
               Input('newPwd2', 'n_submit'),
               Input('newEmail', 'n_submit')],
              [State('newPwd1', 'value'),
               State('newPwd2', 'value')])
def validatePassword2(n_clicks, username_submit, new_password1_submit,
                      new_password2_submit, new_email_submit, new_password1, new_password2):
    if n_clicks > 0 or username_submit > 0 or new_password1_submit > 0 or \
            new_password2_submit > 0 or new_email_submit > 0:
        if new_password1 == new_password2 and len(new_password2) > 7:
            return 'form-control is-valid'
        else:
            return 'form-control is-invalid'
    else:
        return 'form-control'


@app.callback(Output('newEmail', 'className'),
              [Input('createUserButton', 'n_clicks'),
               Input('newUsername', 'n_submit'),
               Input('newPwd1', 'n_submit'),
               Input('newPwd2', 'n_submit'),
               Input('newEmail', 'n_submit')],
              [State('newEmail', 'value')])
def validateEmail(n_clicks, username_submit, new_password1_submit,
                  new_password2_submit, new_email_submit, new_email):
    if n_clicks > 0 or username_submit > 0 or new_password1_submit > 0 or \
            new_password2_submit > 0 or new_email_submit > 0:
        user = Users.query.filter_by(email=new_email).first()
        if new_email is None or new_email == '' or user:
            return 'form-control is-invalid'
        else:
            return 'form-control is-valid'
    else:
        return 'form-control'


@app.callback(Output('createUserSuccess', 'children'),
              [Input('createUserButton', 'n_clicks'),
               Input('newUsername', 'n_submit'),
               Input('newPwd1', 'n_submit'),
               Input('newPwd2', 'n_submit'),
               Input('newEmail', 'n_submit')],
              [State('newUsername', 'value'),
               State('newPwd1', 'value'),
               State('newPwd2', 'value'),
               State('newEmail', 'value'),
               State('admin', 'value')])
def create_user(n_clicks, username_submit, new_password1_submit, new_password2_submit,
                new_email_submit, new_username, new_password1, new_password2, new_email, admin):
    if (n_clicks > 0) or (username_submit > 0) or (new_password1_submit > 0) or \
            (new_password2_submit > 0) or (new_email_submit > 0):
        user_by_email = Users.query.filter_by(email=new_email).first()
        if new_username and new_password1 and new_password2 and new_email != '' and current_user.is_admin and \
                not user_by_email:
            if new_password1 == new_password2:
                if len(new_password1) > 7:
                    try:
                        admin = True if admin == 1 else False
                        hashed_password = generate_password_hash(new_password1, method='sha256')
                        new_user = Users(new_username, new_email, hashed_password, admin)
                        db.session.add(new_user)
                        db.session.commit()
                        return html.Div(children=['New User created'], className='text-success')
                    except Exception as e:
                        return html.Div(children=['New User not created: {e}'.format(e=e)], className='text-danger')
                else:
                    return html.Div(children=['New Password Must Be Minimum 8 Characters'], className='text-danger')
            else:
                return html.Div(children=['Passwords do not match'], className='text-danger')
        else:
            return html.Div(children=['You are not an administrator/User already has an account'],
                            className='text-danger')


@app.callback(Output('urlUserAdmin', 'pathname'),
              [Input('admin-dash', 'n_clicks'),
               Input('admin-profile', 'n_clicks'),
               Input('admin-logout', 'n_clicks')])
def admin_link(n_clicks_dash, n_clicks_profile, n_clicks_logout):
    if n_clicks_dash > 0:
        return '/dashboard'
    elif n_clicks_profile > 0:
        return '/profile'
    elif n_clicks_logout > 0:
        if current_user.is_authenticated:
            logout_user()
            return '/'
        else:
            return '/'


@app.callback(Output('users', 'data'),
              [Input('page-content', 'children'),
               Input('createUserSuccess', 'children')])
def show_users(page_content, create_user_success):
    results = Users.query.order_by(Users.date_created).all()
    users = []
    for result in results:
        users.append({
            'id': result.id,
            'username': result.username,
            'email': result.email,
            'admin': result.is_admin
        })
    return users


@app.callback(Output('output-users', 'children'),
              [Input('users', 'data_previous')],
              [State('users', 'data')])
def show_removed_rows(previous, current):
    if previous is None:
        exceptions.PreventUpdate()
    else:
        rows = [row for row in previous if row not in current]
        row = rows[0]
        row_id = row['id']
        name = row['username']
        if name != current_user.username:
            user_to_delete = Users.query.get_or_404(row_id)
            try:
                db.session.delete(user_to_delete)
                db.session.commit()
                return html.Div(children=[f'{name} is no longer a user'], className='text-success')
            except Exception as e:
                return html.Div(children=['User has not deleted: {e}'.format(e=e)], className='text-danger')
        else:
            return html.Div(children=['You cannot remove yourself!'], className='text-danger')