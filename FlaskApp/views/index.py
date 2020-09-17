from flask import Blueprint, render_template, url_for, request, redirect
from repository.in_memory_data import memory_data, BlogPost, datetime
#from models.BlogPost import BlogPost

index_blueprint = Blueprint('index', __name__)

@index_blueprint.route("/")
@index_blueprint.route("/index")
def index():
    return render_template('index.html', blogs = memory_data)

@index_blueprint.route("/new_post", methods = ['GET', 'POST'])
def new_post():
    if request.method == 'GET':
        return render_template("blog_form.html")

    post = BlogPost(len(memory_data) + 1, request.form.get('title'),
                    request.form.get('contents'), request.form.get('owner'), datetime.now()
                    )
    memory_data.insert(0, post)
    return redirect('/')