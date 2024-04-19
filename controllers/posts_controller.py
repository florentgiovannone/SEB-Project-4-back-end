from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from flask import Blueprint, request, jsonify, g
from models.posts_model import PostModel
from models.like_model import LikeModel
from app import db
from serializers.post_serializer import PostSerializer
from serializers.comment_serializer import CommentSerializer
from middleware.secure_route import secure_route
from serializers.like_serializer import LikeSerializer

like_serializer = LikeSerializer()
post_serializer = PostSerializer()
comment_serializer = CommentSerializer()

router = Blueprint("posts", __name__)


# TODO Get all the post
# ! We need a decorator to specify the route.
@router.route("/posts", methods=["GET"])
def get_posts():
    posts = db.session.query(PostModel).all()
    print(post_serializer.jsonify(posts, many=True))
    return post_serializer.jsonify(posts, many=True)


# TODO Get a post by its ID
@router.route("/posts/<int:post_id>", methods=["GET"])
def get_single_post(post_id):
    post = db.session.query(PostModel).get(post_id)
    if post is None:
        return jsonify({"message": "post not found"}, HTTPStatus.NOT_FOUND)
    return post_serializer.jsonify(post)


# TODO Add a new post
@router.route("posts", methods=["POST"])
@secure_route
def create_post():
    post_dictionary = request.json
    try:
        post_model = post_serializer.load(post_dictionary)
        print(post_model)
        post_model.user_id = g.current_user.id
        db.session.add(post_model)
        db.session.commit()
        return post_serializer.jsonify(post_model)
    except ValidationError as e:
        return {
            "errors": e.message,
            "message": "Something went wrong",
        }, HTTPStatus.BAD_REQUEST
    except Exception as e:
        return {"message": "Something went wrong"}

# TODO Get all likes
# ! We need a decorator to specify the route.
@router.route("/likes", methods=["GET"])
def get_likes():
    likes = db.session.query(LikeModel).all()
    print(like_serializer.jsonify(likes, many=True))
    return like_serializer.jsonify(likes, many=True)

# TODO like a post
@router.route("/posts/<int:post_id>/likes", methods=["POST"])
@secure_route
def like(post_id):
    existing_post = PostModel.query.get(post_id)
    if not existing_post:
        return {"message": "No post found"}, HTTPStatus.NOT_FOUND
    try:
        like = like_serializer.load({})
        like.user_id = g.current_user.id
        like.post_id = post_id
        like.save()
    except ValidationError as e:
        return {
            "errors": e.message,
            "message": "Something went wrong",
        }, HTTPStatus.BAD_REQUEST
    except Exception as e:
        return {"message": "Something went very wrong"}
    return like_serializer.jsonify("Liked")

# TODO dislike a post
@router.route("/likes/<int:like_id>", methods=["DELETE"])
@secure_route
def remove_like(like_id):

    like = LikeModel.query.get(like_id)

    if not like:
        return {"message": "No like found"}, HTTPStatus.NOT_FOUND

    like.remove()
    return {"message": "like Deleted"}, HTTPStatus.OK

# TODO Update a post
@router.route("/posts/<int:post_id>", methods=["PUT"])
@secure_route
def update_post(post_id):

    try:
        post = db.session.query(PostModel).get(post_id)
        if post is None:
            return jsonify({"message": "post not found"}, HTTPStatus.NOT_FOUND)
        if post.user_id != g.current_user.id:
            return {"message": "Go away!!"}
        
        post_data = request.json
        post.title = post_data.get("title", post.title)
        post.content = post_data.get("content", post.content)
        post.category = post_data.get("category", post.category)
        post.image = post_data.get("image", post.image)
        post.code = post_data.get("code", post.code)
        db.session.commit()
        return post_serializer.jsonify(post)

    except ValidationError as e:
        return {
            "errors": e.message,
            "message": "Something went wrong",
        }, HTTPStatus.BAD_REQUEST

    except Exception as e:
        return {"message": "Something went wrong"}, HTTPStatus.BAD_REQUEST


# TODO Delete a post
@router.route("/posts/<int:post_id>", methods=["DELETE"])
@secure_route
def delete_single_post(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        return jsonify({"message": "post not found"}, HTTPStatus.NOT_FOUND)

    post.remove()
    return jsonify({"error":"post deleted"})


@router.route("/posts/<int:post_id>", methods=["DELETE"])
@secure_route
def remove_post(like_id):

    like = LikeModel.query.get(like_id)

    if not like:
        return {"message": "No like found"}, HTTPStatus.NOT_FOUND

    like.remove()
    return {"message": "like Deleted"}, HTTPStatus.OK
