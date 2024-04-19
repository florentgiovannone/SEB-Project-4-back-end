from app import db


class CommentModel(db.Model):

    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    contents = db.Column(db.Text, nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    from models.users_model import UserModel
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    users = db.relationship(UserModel, backref="comments")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()
