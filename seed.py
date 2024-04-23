from flask import Blueprint, request, jsonify, g
from app import app, db
from models.posts_model import PostModel
from models.users_model import UserModel
from models.comment_model import CommentModel
from models.like_model import LikeModel
from datetime import datetime, timedelta, timezone

# getting the current date and time
current_datetime = datetime.now()

# getting the year from the current date and time
current_year = current_datetime.strftime("%Y")
print("current year = ", current_year)

# getting the month from the current date and time
current_month = current_datetime.strftime("%m")
print("current month = ", current_month)

# getting the day/date from the current date and time
current_day = current_datetime.strftime("%d")
print("current day = ", current_day)

# getting the time from the current date and time in the given format
current_time = current_datetime.strftime("%H:%M:%S")
print("current time = ", current_time)

# getting the date and time from the current date and time in the given format
current_date_time = current_datetime.strftime("%d/%m/%Y%H:%M")
print("current date and time = ", current_date_time)


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
            image="https://res.cloudinary.com/ded4jhx7i/image/upload/v1713790251/fhhazkee4tmc4q576hlc.jpg",
        )
        Florent_two = UserModel(
            firstname="Florent",
            lastname="Giovannone",
            username="flo2",
            email="f.giovannon2@me.com",
            password="Hello123",
            password_confirmation="Hello123",
            image="https://res.cloudinary.com/ded4jhx7i/image/upload/v1713790251/fhhazkee4tmc4q576hlc.jpg",
        )

        db.session.add(Florent)
        db.session.add(Florent_two)
        db.session.commit()

        first_post = PostModel(
            title="1st post!",
            content="this is my second post and it's without image",
            image="https://www.adorama.com/alc/wp-content/uploads/2018/11/landscape-photography-tips-yosemite-valley-feature.jpg",
            category="is feeling",
            categoryContent="Proud",
            user_id=Florent.id,
            post_date=current_date_time,
        )
        second_post = PostModel(
            title="2nd post!",
            image="https://www.adorama.com/alc/wp-content/uploads/2018/11/landscape-photography-tips-yosemite-valley-feature.jpg",
            category="is feeling",
            categoryContent="Proud",
            user_id=Florent_two.id,
            post_date=current_date_time,
        )
        third_post = PostModel(
            title="3rd post!",
            content="this is my third post",
            category="is feeling",
            categoryContent="Proud",
            user_id=Florent.id,
            post_date=current_date_time,
        )
        db.session.add(first_post)
        db.session.add(second_post)
        db.session.add(third_post)
        db.session.commit()

        db.session.commit()
        print("seeded!")

    except Exception as e:
        print(e)
