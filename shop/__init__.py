from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_msearch import Search
import os






db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///huellitas7.db"
app.config['SECRET_KEY'] = "huellitasperdidas12345."



app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
app.config['MAX_CONTENT_LENGTH'] = 800 * 1024 * 1024  # Establece el límite a 16 MB (puedes ajustar este valor según tus necesidades)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app) 


db.init_app(app)
search = Search()
search.init_app(app)
bcrypt=Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='userLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message= u"Inicie sesión primero"





from shop.admin import routes
from shop.mascotas import routes
from shop.User import routes





#db.init_app(app)



