"""Routes for the user aspect."""
from flask import (render_template, url_for, flash, redirect, request,
                   Blueprint, abort)
from flask_login import login_user, current_user, logout_user, login_required
from functional import db, bcrypt
from functional.models import User, Post
from functional.users.forms import (RegistrationForm, LoginForm,
                                    UpdateAccountForm, SendEmailForm,
                                    RequestResetForm, ResetPasswordForm)
from functional.users.utils import (save_picture, save_banner,
                                    send_reset_email, send_admin_email,
                                    send_registration_confirmation,
                                    admin_required)

users = Blueprint('users', __name__)
# use users.route instead of app.route.
admins = ['owenthroup@gmail.com', 'lolyougotkilled@gmail.com']


@users.route('/register', methods=['GET', 'POST'])
def register():
    """Handle the registration route."""
    if current_user.is_authenticated:  # if they are already logged in
        return redirect(url_for('main.home'))  # send them back!
    form = RegistrationForm()  # Instance of reg form
    if form.validate_on_submit():  # If the data doesn't conflict
        hashed_password = bcrypt.generate_password_hash(form.password.data)\
                                                            .decode('utf-8')
        if form.email.data in admins:  # if they are in specified admin list
            user = User(username=form.username.data, email=form.email.data,
                        password=hashed_password, is_admin=True,
                        subscribed=form.subscribe.data)
        else:
            user = User(username=form.username.data, email=form.email.data,
                        password=hashed_password,
                        subscribed=form.subscribe.data)  # create user object
        db.session.add(user)  # add user
        db.session.commit()  # commit changes and ADD the user
        send_registration_confirmation(user)
        flash('Account created!', 'success')  # give them a message
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    """Handle the login route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # If user returns something (there is a user) and passwords match in db
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)  # log in the user
            return redirect(url_for('main.home'))
        else:  # if no user is found or password is incorrect
            flash('Login Unsuccessful. Check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    """Handle the log out event."""
    logout_user()  # logout the user
    return redirect(url_for('main.home'))  # send them back home


@users.route("/user/<string:username>/posts")  # takes in username
def user_posts(username):
    """Return all posts by a designated user."""
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """Reset the user's password."""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)  # send them the reset email
        flash('An email has been sent with instructions.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',
                           title='Reset Password',
                           form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """Reset the user's password when they authenticate via email."""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)\
                                                            .decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Password updated!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',
                           title='Reset Password',
                           form=form)


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """Handle the view account request route."""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        if form.banner.data:
            banner_file = save_banner(form.banner.data)
            current_user.banner_file = banner_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route('/admin', methods=['GET', 'POST'])  # used for admin controls page
@admin_required
def admin():
    """Handle the admin route."""
    form = SendEmailForm()
    users = User.query.all()
    if form.validate_on_submit():
        subscribed_users = User.query.filter_by(subscribed=True)
        send_admin_email(form.title.data, form.content.data, subscribed_users)
        flash('Email(s) Sent!', 'success')
        return redirect(url_for('main.home'))
    return render_template('admin.html', form=form, users=users)


@users.route("/user/<string:username>/delete", methods=['GET', 'POST'])
def delete_user(username):
    """Delete a specified user."""
    if current_user.is_admin is False:
        abort(403)  # 403 - Forbidden
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author=user).all()
    db.session.delete(user)
    for post in posts:
        db.session.delete(post)
    db.session.commit()
    flash('User has been deleted!', 'success')
    return redirect(url_for('users.manage_users'))


@users.route("/user/<string:username>", methods=['GET', 'POST'])
@admin_required
def user(username):
    """View user's information."""
    user = User.query.filter_by(username=username).first()
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:  # if change pic
            picture_file = save_picture(form.picture.data)
            user.image_file = picture_file
        if form.banner.data:
            banner_file = save_banner(form.banner.data)
            user.banner_file = banner_file
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    return render_template('user.html', user=user,
                           form=form, image_file=image_file)
