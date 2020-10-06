from datetime import datetime
from flask import Blueprint, render_template, request, redirect
from models.blog_post import BlogPost
from services.services import Services


posts_views_blueprint = Blueprint('post_views', __name__)
POSTS = 'posts'
CONFIG = 'config'

@posts_views_blueprint.route("/")
@posts_views_blueprint.route('/index')
def index():
    posts = Services.get_service(POSTS)
    config = Services.get_service(CONFIG)
    if config.is_configured:
        return render_template('list_posts.html', blogs=posts.get_all())

    return redirect('/setup')

@posts_views_blueprint.route("/new", methods=['GET', 'POST'])
def new_post():
    if request.method == 'GET':
        return render_template("new_post.html")

    posts = Services.get_service(POSTS)
    post = BlogPost(len(posts.get_all()) + 1, request.form.get('title'),
                    request.form.get('contents'), request.form.get('owner')
                    )
    posts.add(post)
    return redirect('/')


@posts_views_blueprint.route("/view/<int:post_id>")
def view_post(post_id):
    posts = Services.get_service(POSTS)
    post = posts.get_by_id(post_id)
    return render_template('view_post.html', post=post)


@posts_views_blueprint.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    posts = Services.get_service(POSTS)
    blog_post = posts.get_by_id(post_id)
    if request.method == 'POST':
        blog_post.title = request.form['title']
        blog_post.contents = request.form['contents']
        blog_post.modified_at = datetime.now()
        posts.edit(blog_post)
        return redirect('/view/{}'.format(blog_post.blog_id))

    return render_template('edit_post.html', post=blog_post)


@posts_views_blueprint.route('/delete/<int:post_id>')
def delete_post(post_id):
    posts = Services.get_service(POSTS)
    posts.remove(post_id)
    return redirect('/')
