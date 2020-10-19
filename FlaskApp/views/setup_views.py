from flask import Blueprint, redirect, render_template, request
from services.services import Services
from models.database_settings import DatabaseSettings



setup_views_blueprint = Blueprint('setup_views', __name__)

@setup_views_blueprint.route("/setup", methods=['GET', 'POST'])
def db_setup():
    database = Services.get_service(Services.database)
    if request.method == 'GET':
        return render_template("db_setup.html")

    form_data = request.form
    setup = DatabaseSettings(form_data['dbname'], form_data['user'], form_data['password'])
    Services.get_service(Services.config).save_dbsettings(setup)
    database.setup()
    return redirect('/index')
