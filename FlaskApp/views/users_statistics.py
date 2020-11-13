from flask import Blueprint, render_template
from services.services import Services
from views.views_decorators.authorization import admin_required

users_statistics_blueprint = Blueprint("users_statistics_blueprint", __name__)


@users_statistics_blueprint.route("/statistics/<user>")
@admin_required
def users_statistics(user):
    statistics_service = Services.get_service(Services.statistics)
    stats = statistics_service.get_user_statistics(user)
    return render_template("user_statistics.html", statistics=stats, user=user)
