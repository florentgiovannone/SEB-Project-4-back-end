from app import db


class PostModel(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=True)
    code = db.Column(db.Text, nullable=True)
    image = db.Column(db.Text, nullable=True)
    category = db.Column(db.Text, nullable=False)
    post_date = db.Column(db.Text, nullable=False)

    from models.comment_model import CommentModel
    comments = db.relationship("CommentModel", backref="comments", cascade="all, delete")

    from models.like_model import LikeModel
    likes = db.relationship("LikeModel", backref="likes", cascade="all, delete")

    # Define relationship with UserModel
    from models.users_model import UserModel
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel", backref="posts")

    def remove(self):
        db.session.delete(self)
        db.session.commit()
