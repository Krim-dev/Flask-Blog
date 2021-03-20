from flask import Blueprint, request, abort, flash, render_template, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Blogpost

posts = Blueprint('posts', __name__)

@posts.route('/post/<int:post_id>')
def post(post_id):
	# post = Blogpost.query.filter_by(id=post_id).first()
	post = Blogpost.query.get_or_404(post_id)
	date_posted = post.date_posted.strftime('%B %d, %Y')
	return render_template('post.html', post=post, date_posted=date_posted, user=current_user)


@posts.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	return render_template('add.html', user=current_user)

@posts.route('/addpost', methods=['POST'])
@login_required
def addpost():
	title = request.form.get('title')
	subtitle = request.form.get('subtitle') 
	content = request.form.get('content')

	post = Blogpost(title=title, subtitle=subtitle, user_id=current_user.id,
			content=content)
	flash('Your posts has been added', 'success')
	db.session.add(post)
	db.session.commit()

	return redirect(url_for('views.home'))

@posts.route('post/<int:post_id>/update-post', methods=['POST', 'GET'])
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

@posts.route('post/<int:post_id>/delete-post', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
	post = Blogpost.query.get_or_404(post_id)
	if post.author.id != current_user.id:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash("Your Post Has Been Successfuly Deleted", 'info')
	return redirect(url_for('views.home'))

