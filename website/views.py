from . import db, mail
from flask_mail import Message
from .models import Blogpost
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, abort, current_app
from flask_login import login_required, current_user
import json

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

@views.route('/post/<int:post_id>')
def post(post_id):
	post = Blogpost.query.filter_by(id=post_id).first()

	date_posted = post.date_posted.strftime('%B %d, %Y')
	return render_template('post.html', post=post, date_posted=date_posted, user=current_user)


@views.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	return render_template('add.html', user=current_user)

@views.route('/addpost', methods=['POST'])
@login_required
def addpost():
	title = request.form.get('title')
	subtitle = request.form.get('subtitle') 
	content = request.form.get('content')

	post = Blogpost(title=title, subtitle=subtitle, user_id=current_user.id,
			content=content)

	db.session.add(post)
	db.session.commit()

	return redirect(url_for('views.home'))

@views.route('post/<int:post_id>/update-post', methods=['POST', 'GET'])
@login_required
def update_post(post_id):
	post = Blogpost.query.get_or_404(post_id)
	if post.author.id != current_user.id:
		abort(403)
	if request.method == 'POST':
		title = request.form.get('title')
		subtitle = request.form.get('subtitle') 
		content = request.form.get('content')

		post.title = title
		post.subtitle = subtitle
		post.content = content
		db.session.commit()
		flash("Your account has been updated", 'info')
		return redirect(url_for('views.home'))
	return render_template('add.html', post=post ,user=current_user)

@views.route('post/<int:post_id>/delete-post', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
	post = Blogpost.query.get_or_404(post_id)
	if post.author.id != current_user.id:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash("Your Post Has Been Successfuly Deleted", 'info')
	return redirect(url_for('views.home'))


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