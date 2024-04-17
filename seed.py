from flask import Blueprint, request, jsonify, g
from app import app, db
from models.posts_model import PostModel
from models.users_model import UserModel
from models.comment_model import CommentModel

with app.app_context():
    try:
        print("connected")
        db.drop_all()
        db.create_all()

        Florent = UserModel(
            firstname="Florent",
            lastname="Giovannone",
            username="flo",
            email="f.giovannone@me.com",
            password="Hello123",
            password_confirmation="Hello123",
            image="https://i.postimg.cc/hGNGWybj/IMG-5063.jpg",
        )

        db.session.add(Florent)
        db.session.commit()



        db.session.add(Florent)
        db.session.commit()
        first_post = PostModel(
            title="1st post!",
            content="this is my second post and it's without image",
            image="https://www.adorama.com/alc/wp-content/uploads/2018/11/landscape-photography-tips-yosemite-valley-feature.jpg",
            code="async function fetchPosts()"
"{ const token = localStorage.getItem('token')"
"const resp = await axios.get(`api/posts`)"
"setPost(resp.data)}console.log(user)",
            category="Proud",
            user_id=Florent.id,
        )

        second_post = PostModel(
            title="2nd post!",
            image="https://www.adorama.com/alc/wp-content/uploads/2018/11/landscape-photography-tips-yosemite-valley-feature.jpg",
            category="Proud",
            user_id=Florent.id,
        )

        third_post = PostModel(
            title="3rd post!",
            content="this is my third post",
            category="Proud",
            user_id=Florent.id,
        )

        

        db.session.add(first_post)
        db.session.add(second_post)
        db.session.add(third_post)
        db.session.commit()

        first_comment = CommentModel(
            content="Loving it 1!!",
            post_id=first_post.id,
            user_id=Florent.id
        )
        second_comment = CommentModel(
            content="Loving it 2!!",
            post_id=second_post.id,
            user_id=Florent.id
        )
        third_comment = CommentModel(
            content="Loving it 3!!",
            post_id=third_post.id,
            user_id=Florent.id
        )

        db.session.add(first_comment)
        db.session.add(second_comment)
        db.session.add(third_comment)
        db.session.commit()
        print("seeded!")

    except Exception as e:
        print(e)
