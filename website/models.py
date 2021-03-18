from . import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.sql import func

class Blogpost(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50))
	subtitle = db.Column(db.String(50))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	date_posted = db.Column(db.DateTime, default=func.now())
	content = db.Column(db.Text)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(150), unique=True)
	password = db.Column(db.String(150))
	first_name = db.Column(db.String(150))
	notes = db.relationship('Blogpost', backref='author', lazy=True)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None

		return User.query.get(user_id)