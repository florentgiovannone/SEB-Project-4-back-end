

from app import db


class CommentModel(db.Model):

    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    content = db.Column(db.Text, nullable=False)
    comment_date = db.Column(db.Text, nullable=False)
    code = db.Column(db.Text, nullable=True)

    # ! ForeignKey tells you which column to point at (teas.id)
    # ! so that every comment points to a specific unique tea.
    # ! You usually give it the primarykey of a table, e.g. teas.id
    from models.posts_model import PostModel
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    post = db.relationship(PostModel, backref="comment")

    from models.users_model import UserModel
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship(UserModel, backref="comment")

    def save(self):
        db.session.add(self)
        db.session.commit()

    # ! Added little method to call SQLAlchemy commands to delete my model.
    def remove(self):
        db.session.delete(self)
        db.session.commit()
