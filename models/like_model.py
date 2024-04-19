from app import db


class LikeModel(db.Model):

    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True, unique=True)

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    from models.users_model import UserModel
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    users = db.relationship("UserModel", backref="likes")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()
