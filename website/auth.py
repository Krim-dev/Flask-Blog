from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
	if current_user.is_authenticated:
		flash('You are already logged in', 'info')
		return redirect(url_for('views.home'))

	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')

		user = User.query.filter_by(email=email).first()
		if user:
			if check_password_hash(user.password, password):
				login_user(user, remember=True)
				next_page = request.args.get('next')
				flash('Logged in successfully', category='success')
				return redirect(next_page) if next_page else redirect(url_for('views.home'))
			else:
				flash('Incorrect Passord Try Again', 'warning')
		else:
			flash('Email Does Not Exist', 'warning')
	return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
	flash(f'You were logged out {current_user.first_name}', 'danger')
	logout_user()
	return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
	if current_user.is_authenticated:
		flash('You are already logged in', 'info')
		return redirect(url_for('views.home'))

	if request.method == 'POST':
		email = request.form.get('email')
		firstName = request.form.get('firstName')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')

		user = User.query.filter_by(email=email).first()
		if user:
			flash('Email Is Already Taken', category='info')
		elif len(email) < 4 :
			flash('Email must be greater than 3 characters', category='warning')
		elif len(firstName) < 2:
			flash('First Name be greater than 1 characters', category='warning')
		elif password1 != password2:
			flash('Password don\'t match ', category='danger')
		elif len(password1) < 7:
			flash('Password must be at least 7 charachters', category='danger')
		else:
			new_user = User(email=email, first_name=firstName,
				 	password=generate_password_hash(password1, method='sha256'))
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user, remember=True)
			flash(f'Account created for {firstName}', 'success')
			return redirect(url_for('views.home'))

	return render_template('sign_up.html', user=current_user)


@auth.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	if request.method == 'POST':
		current_user.first_name = request.form.get('first_name')
		current_user.email = request.form.get('email')
		db.session.commit()
		flash("Your account has been updater successfully ", 'success')
	return render_template('account.html', user=current_user)

# @auth.route('/reset')