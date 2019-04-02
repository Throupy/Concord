"""Main application routes."""
from flask import render_template, request, Blueprint
from functional.models import Post

main = Blueprint('main', __name__)
# use main.route instead of app.route.


@main.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,
                                                                  per_page=4)
    return render_template("home.html", posts=posts)
