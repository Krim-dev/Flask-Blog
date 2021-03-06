import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_mail import Mail
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'You need to login first'
login_manager.login_message_category = 'info'
DB_NAME = "database.db"
mail = Mail()

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'akfaksamfnkask'
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
	app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
	app.config['MAIL_PORT'] = 587
	app.config['MAIL_USE_TLS'] = True
	app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
	app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
	db.init_app(app)

	from .views import views
	from .auth import auth
	from .handlers import errors
	from .posts import posts

	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')
	app.register_blueprint(errors)
	app.register_blueprint(posts, url_prefix='/')

	from .models import User

	create_database(app)
	login_manager.init_app(app)
	mail.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))

	return app


def create_database(app):
	if not path.exists('website/' + DB_NAME):
		db.create_all(app=app)
		print('Created Database!')