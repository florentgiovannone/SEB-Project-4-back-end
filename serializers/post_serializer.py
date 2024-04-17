from app import marshy
from models.posts_model import PostModel
from marshmallow import fields
from serializers.user_serializer import UserSerializer
from serializers.comment_serializer import CommentSerializer


class PostSerializer(marshy.SQLAlchemyAutoSchema):
    comment = fields.Nested("CommentSerializer", many=True)
    user = fields.Nested("UserSerializer", many=False)

    class Meta:
        model = PostModel
        load_instance = True
