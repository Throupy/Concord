from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from functional import db
from functional.models import Post
from functional.posts.forms import PostForm

posts = Blueprint('posts', __name__)
# use posts.route instead of app.route.


@posts.route("/post/<int:post_id>")  # site.com/post/1 will be post 1, post/2 = post 2 etc (each post has an ID)
def post(post_id):
    post = Post.query.get_or_404(post_id)  # get post with that ID. If it can't it will return a 404 error.
    return render_template('post.html', title=post.title, post=post, legend='New Post')


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)  # get post with that ID. If it can't it will return a 404 error.
    if post.author != current_user and current_user.is_admin == False:  # If the current user is NOT the author
        abort(403)  # 403 - Forbidden
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()  # don't need to add cos it's already in the database
        flash("post has been modified!", "success")
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')  # I can use create post form cos it's the same shit we want


@posts.route('/posts/search/', methods=['GET', 'POST'])
def search_posts():
    if request.method == 'POST':
        text = request.form.get('search', None)
        posts = Post.query.filter(Post.title.contains(text) | Post.content.contains(text)).all()
        return render_template('searched_posts.html', posts=posts)
    return redirect('account')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])  # Only accept when they submit the delete request
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)  # get post with that ID. If it can't it will return a 404 error.
    if post.author != current_user and current_user.is_admin == False:  # If the current user is NOT the author and is NOT an admin
        abort(403)  # 403 - Forbidden
    db.session.delete(post)  # delete
    db.session.commit()  # DELETE
    flash('post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():  # make sure no errors
        post = Post(title=form.title.data, content=form.content.data, author=current_user)  # set instance with vals from form
        db.session.add(post)  # add
        db.session.commit()  # ADD
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form)
