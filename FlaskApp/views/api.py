from flask import Blueprint, abort, jsonify
from services.services import Services


api_blueprint = Blueprint("api_blueprint", __name__)


@api_blueprint.route("/api/post/<post_id>", methods=["GET"])
def get_post(post_id):
    posts = Services.get_service(Services.posts)
    post = posts.get_by_id(post_id)
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