from exceptions.exceptions import SectionNotFoundError
from flask import Flask
from views.posts_views import posts_views_blueprint
from views.setup_views import setup_views_blueprint
from views.login_views import login_views_blueprint
from views.users_views import users_views_blueprint, Services

application = Flask(__name__)
application.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

application.register_blueprint(posts_views_blueprint)
application.register_blueprint(setup_views_blueprint)
application.register_blueprint(login_views_blueprint)
application.register_blueprint(users_views_blueprint)


@application.before_first_request
def update_to_latest_version():
    database = Services.get_service(Services.database)
    try:
        if database.new_version_available():
            database.update()
    except SectionNotFoundError:
        pass


if __name__ == '__main__':
    application.run('localhost', 4449)
