from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from flask import Blueprint, request, jsonify, g
from models.comment_model import CommentModel
from models.posts_model import PostModel
from app import db
from serializers.comment_serializer import CommentSerializer
from middleware.secure_route import secure_route

comment_serializer = CommentSerializer()

router = Blueprint("comnments", __name__)

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

    existing_tea = PostModel.query.get(post_id)
    if not existing_tea:
        return {"message": "No tea found"}, HTTPStatus.NOT_FOUND

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
