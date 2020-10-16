from flask import Blueprint, redirect, render_template, request
from services.services import Services
from models.database_settings import DatabaseSettings
from setup.database import Database
from setup.dbconfig import DbConfig



setup_views_blueprint = Blueprint('setup_views', __name__)

@setup_views_blueprint.route("/setup", methods=['GET', 'POST'])
def db_setup():
    database = Database(DbConfig('postgres'))
    if request.method == 'GET':
        if not Services.TESTING:
            database.update()
            return redirect('/index')
        return render_template("db_setup.html")

    form_data = request.form
    setup = DatabaseSettings(form_data['dbname'], form_data['user'], form_data['password'])
    Services.get_service(Services.config).save_dbsetup(setup)
    database.setup()
    return redirect('/index')
