# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from flask import Flask
from views.posts_views import posts_views_blueprint

application = Flask(__name__)
application.register_blueprint(posts_views_blueprint)

if __name__ == '__main__':
    application.run('localhost', 4449)
