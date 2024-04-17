from app import db


class PostModel(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.Text, nullable=False, )
    content = db.Column(db.Text, nullable=True)
    code = db.Column(db.Text, nullable=True)
    image = db.Column(db.Text, nullable=True)
    category = db.Column(db.Text, nullable=False)

    from models.users_model import UserModel
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship(UserModel, backref="posts")

