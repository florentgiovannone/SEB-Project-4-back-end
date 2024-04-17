from http import HTTPStatus
from flask import Blueprint, request, jsonify, g
from marshmallow.exceptions import ValidationError
from app import db
from models.users_model import UserModel
from serializers.user_serializer import UserSerializer
from datetime import datetime, timedelta, timezone
from config.environment import SECRET
import jwt
from middleware.secure_route import secure_route
import re


user_serializer = UserSerializer()
router = Blueprint("users", __name__)


@router.route("/signup", methods=["POST"])
def signup():
    try:
            user_dictionary = request.json
            email = user_dictionary.get('email')
            password = user_dictionary.get('password')
            password_confirmation = user_dictionary.get('password_confirmation')
            if password != password_confirmation:
                return jsonify({'error': 'Passwords do not match'}), 400
            else:
                user_model = user_serializer.load(user_dictionary)
                db.session.add(user_model)
                db.session.commit()
                return user_serializer.jsonify(user_model)
    except ValidationError as e:
        return jsonify ({
            "error": "Something went wrong",
        }), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return {"error": "Something went very wrong"}


@router.route("/login", methods=["POST"])
def login():
    credentials_dictionary = request.json
    user = (
        db.session.query(UserModel)
        .filter_by(username=credentials_dictionary["username"])
        .first()
    )
    if not user:
        return jsonify({"error": "Login failled. Try again"})
    if not user.validate_password(credentials_dictionary["password"]):
        return jsonify({"error": "Login failled. Try again"})

    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(days=1),
        "iat": datetime.now(timezone.utc),
        "sub": user.id,
    }

    secret = SECRET

    token = jwt.encode(payload, secret, algorithm="HS256")
    return {"message": "Login successful.", "token": token}


@router.route("/user", methods=["GET"])
@secure_route
def get_current_user():
    try:
        user = db.session.query(UserModel).get(g.current_user.id)
        print(user_serializer.jsonify(user))
        return user_serializer.jsonify(user)
    except ValidationError as e:
        return {
            "errors": e.messages,
            "message": "Something went wrong",
        }, HTTPStatus.BAD_REQUEST
    except Exception as e:
        return {"message": "Something went very wrong"}


@router.route("/users", methods=["GET"])
def get_current_users():
    user = db.session.query(UserModel).all()
    print(user_serializer.jsonify(user, many=True))
    return user_serializer.jsonify(user, many=True)


@router.route("/users/<int:user_id>", methods=["GET"])
def get_single_user(user_id):
    post = db.session.query(UserModel).get(user_id)
    if post is None:
        return jsonify({"message": "user not found"}, HTTPStatus.NOT_FOUND)
    return user_serializer.jsonify(post)


@router.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        user = db.session.query(UserModel).get(user_id)
        if user is None:
            return jsonify({"message": "user not found"}, HTTPStatus.NOT_FOUND)       
        user_data = request.json
        user.firstname = user_data.get("firstname", user.firstname)
        user.lastname = user_data.get("lastname", user.lastname)
        user.username = user_data.get("username", user.username)
        user.email = user_data.get("email", user.email)
        user.image = user_data.get("image", user.image)
        db.session.commit()
        return user_serializer.jsonify(user)

    except ValidationError as e:
        return {
            "errors": e.message,
            "message": "Something went wrong",
        }, HTTPStatus.BAD_REQUEST

    except Exception as e:
        return {"message": "Something went very wrong"}, HTTPStatus.BAD_REQUEST
    
    
