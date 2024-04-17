from app import marshy
from marshmallow import fields
from models.comment_model import CommentModel



class CommentSerializer(marshy.SQLAlchemyAutoSchema):
    user = fields.Nested("UserSerializer", many=False)

    class Meta:
        model = CommentModel
        load_instance = True
