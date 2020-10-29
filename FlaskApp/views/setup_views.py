from flask import Blueprint, redirect, request, abort
from services.services import Services
from models.database_settings import DatabaseSettings

setup_views_blueprint = Blueprint('setup_views', __name__)


@setup_views_blueprint.route("/setup", methods=['POST'])
def db_setup():
    database = Services.get_service(Services.database)
    if database.config.is_configured:
        return abort(403)
    form_data = request.form
    setup = DatabaseSettings(form_data['dbname'], form_data['user'], form_data['password'])
    Services.get_service(Services.config).save_dbsettings(setup)
    database.setup()
    return redirect('/index')
