import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

# Default variable
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'media')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Flask app initialization
app = Flask(__name__,template_folder='templates',static_folder='Static')
app.debug = True if os.environ.get("DEBUG") == 'True' else False

# Flask Config
app.secret_key = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Data-Base settings
db = SQLAlchemy(app)
migrate = Migrate(app,db)

# CSRF protection
csrf = CSRFProtect(app)

# E-Mail Configuration
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("MAIL_USERNAME")
mail = Mail(app)

# Authentication Settings
login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = "auth_views.login"
login_manager.login_message_category = "info"
bcrypt = Bcrypt(app)  # Password Encryption

# BluePrint Register
from .apps.crud.views import crud_views as crud_blueprint
from .apps.authentication.views import auth_views as auth_blueprint
from .apps.user_profile.views import profile_views as profile_blueprint

app.register_blueprint(crud_blueprint,url_prefix = '')
app.register_blueprint(auth_blueprint,url_prefix = '/auth')
app.register_blueprint(profile_blueprint,url_prefix = '/profile')