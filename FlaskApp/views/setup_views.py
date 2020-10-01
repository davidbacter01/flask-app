from flask import Blueprint, render_template, redirect, request


setup_views_blueprint = Blueprint('setup_views', __name__)

@setup_views_blueprint.route("/setup", methods=['GET', 'POST'])
def db_setup():
    if request.method == 'GET':
        return render_template("db_setup.html")

    return redirect('/')
