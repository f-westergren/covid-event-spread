from flask_login import UserMixin
from flask_bcrypt import Bcrypt

from app import db, login

bcrypt = Bcrypt()

class User(UserMixin, db.Model):
	""" Users """

	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False, unique=True)
	location = db.Column(db.String)
	password = db.Column(db.Text, nullable=False)

	def __repr__(self):
		return f'<User id={self.id} name={self.name}>'
	
	@classmethod
	def register(cls, email, password, name, location=''):
		"""Register user with hashed password and return user"""
	
		hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

		user = User(
			email=email,
			password=hashed_pwd,
			name=name,
			location=location
		)
		
		db.session.add(user)
		return user

	@classmethod
	def authenticate(cls, email, password):
		"""Validate that user exists & password is correct.

		Return user if valid, else return false.
		"""
		u = User.query.filter_by(email=email).first()

		if u and bcrypt.check_password_hash(u.password, password):
			#return user instance
			return u
		else:
			return False
			
class Search(db.Model):
	""" Searches """

	__tablename__ = 'searches'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	location = db.Column(db.String, nullable=False)
	search_date = db.Column(db.DateTime, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False)
	description = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

	def __repr__(self):
		return f'<Search id={self.id} location={self.location} search_date={self.search_date} user_id={self.user_id}>'

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
		