from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
app = Flask(__name__)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hello_world'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'noone'
    app.config['MAIL_PASSWORD'] = 'nicetry'
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    from functional.users.routes import users  # import the blueprint
    from functional.posts.routes import posts  # import the blueprint
    from functional.main.routes import main  # import the blueprint
    from functional.errors.handlers import errors
    app.register_blueprint(users)  # register the blueprint
    app.register_blueprint(posts)  # register the blueprint
    app.register_blueprint(main)  # register the blueprint
    app.register_blueprint(errors)
#    with app.app_context():
#        db.create_all()
#        db.session.commit()

    return app
