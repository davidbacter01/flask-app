from flask import Blueprint, redirect, render_template, request
from services.services import Services



setup_views_blueprint = Blueprint('setup_views', __name__)

@setup_views_blueprint.route("/setup", methods=['GET', 'POST'])
def db_setup():
    posts = Services.get_service(Services.posts)
    if request.method == 'GET':
        return render_template("db_setup.html")

    form_data = request.form
    posts.database.config.save_configuration(form_data)
    posts.database.setup()
    return redirect('/')
