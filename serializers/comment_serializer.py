from app import marshy
from marshmallow import fields
from models.comment_model import CommentModel
from serializers.like_serializer import LikeSerializer
from serializers.user_serializer import UserSerializer

class CommentSerializer(marshy.SQLAlchemyAutoSchema):
    user = fields.Nested("UserSerializer", many=False)


    class Meta:
        model = CommentModel
        load_instance = True