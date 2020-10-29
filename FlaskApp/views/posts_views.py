from datetime import datetime
import math
from flask import Blueprint, render_template, request, redirect, session
from models.blog_post import BlogPost
from services.services import Services
from views.views_decorators.authorization import login_required, admin_or_post_owner_required
from views.views_decorators.setup_required import setup_required

posts_views_blueprint = Blueprint('post_views', __name__)


@posts_views_blueprint.route("/")
@posts_views_blueprint.route('/index')
@setup_required
def index():
    owner = request.args.get('owner')
    page = request.args.get('page')
    posts_service = Services.get_service(Services.posts)
    total_pages = math.ceil(posts_service.count(owner) / 5)
    try:
        if int(page) < 1 or int(page) > int(total_pages):
            page = 1
    except TypeError:
        page = 1
    except ValueError:
        page = 1
    posts = posts_service.get_all(owner, page)
    users = Services.get_service(Services.users).get_all()
    return render_template('list_posts.html',
                           blogs=posts,
                           users=users,
                           filter=owner,
                           page=int(page),
                           total=total_pages)


@posts_views_blueprint.route("/new", methods=['GET', 'POST'])
@setup_required
@login_required
def new_post():
    if request.method == 'GET':
        return render_template("new_post.html")

    posts = Services.get_service(Services.posts)
    post = BlogPost(request.form.get('title'),
                    request.form.get('contents'), session['user_id']
                    )
    posts.add(post)
    return redirect('/index')


@posts_views_blueprint.route("/view/<int:post_id>")
@setup_required
def view_post(post_id):
    posts = Services.get_service(Services.posts)
    post = posts.get_by_id(post_id)
    return render_template('view_post.html', post=post)


@posts_views_blueprint.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@setup_required
@login_required
@admin_or_post_owner_required
def edit_post(post_id):
    posts = Services.get_service(Services.posts)
    blog_post = posts.get_by_id(post_id)
    if request.method == 'POST':
        blog_post.owner = session['user_id']
        blog_post.title = request.form['title']
        blog_post.contents = request.form['contents']
        blog_post.modified_at = datetime.now()
        posts.edit(blog_post)
        return redirect('/view/{}'.format(blog_post.blog_id))

    return render_template('edit_post.html', post=blog_post)


@posts_views_blueprint.route('/delete/<int:post_id>')
@setup_required
@login_required
@admin_or_post_owner_required
def delete_post(post_id):
    posts = Services.get_service(Services.posts)
    posts.remove(post_id)
    return redirect('/index')
