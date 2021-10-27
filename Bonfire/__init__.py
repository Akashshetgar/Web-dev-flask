from flask import Flask
from flask_login.utils import login_fresh
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO,send
import socketio

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'e702ae853a110c6e239a8be9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BonfireDB.db'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "loginPage"
login_manager.login_message_category = "info"
db = SQLAlchemy(app)

from Bonfire import routes