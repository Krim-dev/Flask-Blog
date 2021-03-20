from . import mail
from flask_mail import Message
from .models import Blogpost
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

views = Blueprint('views', __name__)
@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
	posts = Blogpost.query.all()
	posts.reverse()
	return render_template('home.html', user=current_user, posts=posts)

@views.route('/about')
def about():
	return render_template('about.html', user=current_user)


@views.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
	if request.method == 'POST':
		name = current_user.first_name
		email = current_user.email
		phone = request.form.get('phone')
		message = request.form.get('message')

		msg = Message(f'Contact from {name}',
						sender='contact@akramweb.com',
						recipients=['samielomrani73@gmail.com'])
		msg.body = f"""{message}\n
email : {email}
Phone : {phone}
"""
		mail.send(msg)
		flash("Your message has been sent we will response as soon as we can", 'info')
		return redirect(url_for('views.home'))
	return render_template('contact.html', user=current_user)