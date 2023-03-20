import os
import warnings

import dash_bootstrap_components as dbc
from dash import Dash
from flask_login import LoginManager
from flask_migrate import Migrate

from config import DATABASE_URI
from models import Users, db



warnings.filterwarnings("ignore")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = 'HPV Monitor Dashboard'
app.update_title = 'Loading...'
app.config.suppress_callback_exceptions = True
app._favicon = 'favicon.ico'

server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI=DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db.init_app(server)
migrate = Migrate()
migrate.init_app(app, db)

login_manager = LoginManager()
login_manager.init_app(server)


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return Users.query.get(user_id)
    return None
