# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from datetime import datetime
from flask import Blueprint, render_template, request, redirect
from repository.in_memory_data import memory_data, BlogPost


def find_post(post_id):
    for blog_post in memory_data:
        if blog_post.id == post_id:
            return blog_post

    return None


index_blueprint = Blueprint('index', __name__)

@index_blueprint.route("/")
@index_blueprint.route('/index')
def index():
    return render_template('index.html', blogs = memory_data)

@index_blueprint.route("/new", methods = ['GET', 'POST'])
def new_post():
    if request.method == 'GET':
        return render_template("blog_form.html")

    post = BlogPost(len(memory_data) + 1, request.form.get('title'),
                    request.form.get('contents'), request.form.get('owner')
                    )
    post.created_at = datetime.now()
    memory_data.insert(0, post)
    return redirect('/')


@index_blueprint.route("/view/<int:post_id>")
def view_post(post_id):
    post = find_post(post_id)
    return render_template('blog_post.html', post = post)

@index_blueprint.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    blog_post = find_post(post_id)
    if request.method == 'POST':
        for blog_post in memory_data:
            if blog_post.id == post_id:
                blog_post.title = request.form['title']
                blog_post.contents = request.form['contents']
                blog_post.modified_at = datetime.now()
                return redirect('/view/{}'.format(blog_post.id))

    return render_template('edit_form.html', post = blog_post)

@index_blueprint.route('/delete/<int:post_id>')
def delete_post(post_id):
    post = find_post(post_id)
    memory_data.remove(post)
    return redirect('/')
