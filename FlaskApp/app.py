from flask import Flask
from views.posts_views import posts_views_blueprint
from views.setup_views import setup_views_blueprint
from views.log_views import log_views_blueprint
from views.user_views import user_views_blueprint

application = Flask(__name__)
application.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

application.register_blueprint(posts_views_blueprint)
application.register_blueprint(setup_views_blueprint)
application.register_blueprint(log_views_blueprint)
application.register_blueprint(user_views_blueprint)


if __name__ == '__main__':
    application.run('localhost', 4449)
