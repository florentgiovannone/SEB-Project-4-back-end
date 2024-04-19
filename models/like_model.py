from app import db


class LikeModel(db.Model):

    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True, unique=True)

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    from models.users_model import UserModel
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel", backref="like")

    # from models.comment_model import CommentModel
    # comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=False)
    # comment = db.relationship(CommentModel, backref="like")

    def save(self):
        db.session.add(self)
        db.session.commit()

    # ! Added little method to call SQLAlchemy commands to delete my model.
    def remove(self):
        db.session.delete(self)
        db.session.commit()
