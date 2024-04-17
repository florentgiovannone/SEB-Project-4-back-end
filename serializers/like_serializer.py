from app import marshy
from marshmallow import fields
from models.like_model import LikeModel
from serializers.user_serializer import UserSerializer


class LikeSerializer(marshy.SQLAlchemyAutoSchema):
    user = fields.Nested("UserSerializer")

    class Meta:
        model = LikeModel
        load_instance = True