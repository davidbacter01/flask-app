from flask import Blueprint, abort, jsonify
from services.services import Services
from views.views_decorators.setup_required import setup_required


api_blueprint = Blueprint("api_blueprint", __name__)


@api_blueprint.route("/api/post/<post_id>", methods=["GET"])
@setup_required
def get_post(post_id):
    posts = Services.get_service(Services.posts)
    post = posts.get_by_id(int(post_id))
    if post is None:
        return abort(404)
    return jsonify({
        "post_id":post.blog_id,
        "title":post.title,
        "owner":post.owner,
        "contents":post.contents,
        "image":post.image,
        "created_at":post.created_at,
        "modified_at":post.modified_at
        })
