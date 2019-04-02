import os
import secrets
from PIL import Image
from flask import url_for, current_app, abort, redirect
from flask_login import current_user
from flask_mail import Message
from functional import mail
from functools import wraps


def save_picture(form_picture):
  random_hex = secrets.token_hex(16)  # to save in profile pics folder
  _, f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_hex + f_ext  # fix
  picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

  output_size = (125, 125)
  i = Image.open(form_picture).convert('RGB')
  i.thumbnail(output_size)
  i.save(picture_path)

  return picture_fn


def save_banner(form_picture):
  random_hex = secrets.token_hex(16)  # to save in profile pics folder
  _, f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_hex + f_ext  # fix
  picture_path = os.path.join(current_app.root_path, 'static/banner_pics', picture_fn)

  output_size = (350, 205)
  i = Image.open(form_picture).convert('RGB')
  i.thumbnail(output_size)
  i.save(picture_path)

  return picture_fn


def send_admin_email(title, content, users):
  with mail.connect() as conn:
    for user in users:
      msg = Message(recipients=[user.email],
                    body='Hello, {} \n {}'.format(user.username, content),
                    subject=title,
                    sender='throupyswebsite@gmail.com')
      conn.send(msg)


def send_registration_confirmation(user):
  msg = Message('Thanks for joining!',
                sender='throupyswebsite@gmail.com',
                recipients=[user.email])
  msg.body = 'Hello %s. Thanks for registering.' % user.username
  mail.send(msg)


def send_reset_email(user):  # take in user
  token = user.get_reset_token()
  msg = Message('Password Reset Request',
                sender='throupyswebsite@gmail.com',
                recipients=[user.email])
  msg.body = '''To reset your password, visit the following link:
{}
If you did not make this request then simply ignore this email and no changes will be made
    '''.format(url_for('users.reset_token', token=token, _external=True))  # external gets the full domain not jsut the relative one
  mail.send(msg)


def admin_required(func):
  @wraps(func)
  def func_wrapper(*args, **kwargs):
    if not current_user.is_authenticated or not current_user.is_admin:
      abort(403)
    return func(*args, **kwargs)
  return func_wrapper
