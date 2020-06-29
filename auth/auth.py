from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.urls import url_parse
from sqlalchemy.exc import IntegrityError
from forms import LoginForm, SignupForm
from models import User, db

auth_bp = Blueprint('auth_bp', __name__,
  template_folder='templates',
  static_folder='static'
)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
	""" Show login page with login form """

	if current_user.is_authenticated:
		return redirect(url_for('index'))
	
	form = LoginForm()

	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		user = User.authenticate(username, password)

		if user:
			login_user(user)
			next_page = request.args.get('next')
			if not next_page or url_parse(next_page).netloc != '':
				next_page = url_for('index')
			return redirect(next_page)
		
		flash("Invalid credentials.", 'danger')

	return render_template('/login.html', form=form, btnText="Sign In", cancel='index')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
	"""Handle user signup.

  Create new user and add to DB. Redirect to home page.

  If form not valid, present form.

  If the there already is a user with that username: flash message
  and re-present form.
  """

	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = SignupForm()

	if form.validate_on_submit():
		try:
			user = User.signup(
				username=form.username.data,
				password=form.password.data,
				email=form.email.data,
			)
			db.session.commit()

		except IntegrityError:
			flash('Username already taken', 'danger')
			return render_template('/signup.html', form=form)
		
		login_user(user)
		return redirect(url_for('index'))
	
	return render_template('signup.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))