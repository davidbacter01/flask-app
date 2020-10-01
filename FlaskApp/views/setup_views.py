from flask import Blueprint, render_template, redirect, request
from views.posts_views import posts

setup_views_blueprint = Blueprint('setup_views', __name__)

@setup_views_blueprint.route("/setup", methods=['GET', 'POST'])
def db_setup():
    if request.method == 'GET':
        return render_template("db_setup.html")

    form_data = request.form
    posts.config.save_configuration(form_data)
    return redirect('/')
