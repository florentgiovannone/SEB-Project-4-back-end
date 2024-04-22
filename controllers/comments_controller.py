from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from flask import Blueprint, request, jsonify, g
from models.comment_model import CommentModel
from models.posts_model import PostModel
from app import db
from serializers.comment_serializer import CommentSerializer
from serializers.like_serializer import LikeSerializer

from middleware.secure_route import secure_route

comment_serializer = CommentSerializer()
like_serializer = LikeSerializer()


router = Blueprint("comments", __name__)


@router.route("/comments", methods=["GET"])
def get_comments():
    comments = db.session.query(CommentModel).all()
    print(comment_serializer.jsonify(comments, many=True))
    return comment_serializer.jsonify(comments, many=True)


@router.route("/comments/<int:comment_id>", methods=["GET"])
def get_single_comment(comment_id):
    comment = db.session.query(CommentModel).get(comment_id)
    if comment is None:
        return jsonify({"message": "comment not found"}, HTTPStatus.NOT_FOUND)
    return comment_serializer.jsonify(comment)


@router.route("/posts/<int:post_id>/comments", methods=["POST"])
@secure_route
def create_comment(post_id):

    comment_dictionary = request.json

    existing_post = PostModel.query.get(post_id)
    if not existing_post:
        return {"message": "No post found"}, HTTPStatus.NOT_FOUND

    try:
        comment = comment_serializer.load(comment_dictionary)
        comment.user_id = g.current_user.id
        comment.post_id = post_id
        comment.save()
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}

    return comment_serializer.jsonify(comment), HTTPStatus.CREATED

@router.route("/comments/<int:comment_id>", methods=["DELETE"])
@secure_route
def remove_comment(comment_id):

    comment = CommentModel.query.get(comment_id)
    if not comment:
        return {"message": "No comment found"}, HTTPStatus.NOT_FOUND
    comment.remove()
    return {"message": "Comment Deleted"}, HTTPStatus.OK


# TODO like a comment
@router.route("/comments/<int:comment_id>/likes", methods=["POST"])
@secure_route
def like_comment(comment_id):
    existing_comment = CommentModel.query.get(comment_id)
    print(existing_comment)
    if not existing_comment:
        return {"message": "No comment found"}, HTTPStatus.NOT_FOUND
    try:
        like = like_serializer.load({})
        like.user_id = g.current_user.id
        like.comment_id = comment_id
        like.save()
    except ValidationError as e:
        return {
            "errors": e.message,
            "message": "Something went wrong",
        }, HTTPStatus.BAD_REQUEST
    except Exception as e:
        return {"message": "Something went very wrong"}, HTTPStatus.BAD_REQUEST
    return like_serializer.jsonify("Liked")


# TODO Update a comment
@router.route("/comments/<int:comment_id>", methods=["PUT"])
@secure_route
def update_comment(comment_id):

    try:
        comment = db.session.query(CommentModel).get(comment_id)
        if comment is None:
            return jsonify({"message": "comment not found"}, HTTPStatus.NOT_FOUND)
        if comment.user_id != g.current_user.id:
            return {"message": "Go away!!"}

        comment_data = request.json
        comment.content = comment_data.get("content", comment.content)
        db.session.commit()
        return comment_serializer.jsonify(comment)

    except ValidationError as e:
        return {
            "errors": e.message,
            "message": "Something went wrong",
        }, HTTPStatus.BAD_REQUEST

    except Exception as e:
        return {"message": "Something went wrong"}, HTTPStatus.BAD_REQUEST
