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

        def validate_field(field_name, error_message):
            value = user_dictionary.get(field_name)
            if not value:
                raise ValidationError({field_name: error_message})
            return value

        def validate_password(password, comnfrim_password):
            spec_chart = ["!", "@", "#", "$", "%", "&", "*"]
            if password != comnfrim_password:
                raise ValidationError({"password_confirmation": "Password do not match"})
            if not ( 8 <= len(password) <= 20):
                raise ValidationError(
                    {"password": "Password needs to be between 8 and 20 characters long"})
            if not re.search("[a-z]", password):
                raise ValidationError(
                    {"password": "Password needs to contain at least 1 lowercase letter"})
            if not re.search("[A-Z]", password):
                raise ValidationError(
                    {"password": "Password needs to contain at least 1 uppercase letter"})
            if not re.search("[0-9]", password):
                raise ValidationError(
                    {"password": "Password needs to contain at least 1 digit"}
                )
            if not any(char in spec_chart for char in password):
                raise ValidationError(
                    {"password": "Password needs to contain at least 1 special character"}
                )
            
        validate_field("firstname", "You need to enter a firstname")
        validate_field("lastname", "You nees to enter a lastname")
        email = validate_field("email", "You nees to enter a email")
        username = validate_field("username", "You nees to enter a username")
        password = validate_field("password", "You nees to enter a password")
        password_confirmation = validate_field("password_confirmation", "You nees to confirm your password")

        if db.session.query(UserModel).filter_by(email=email).first():
            return jsonify({"error": "The email already exists"}), HTTPStatus.BAD_REQUEST
        if db.session.query(UserModel).filter_by(username=username).first():
            return jsonify({"error": "The username already exists"}), HTTPStatus.BAD_REQUEST
        
        validate_password(password, password_confirmation)

        user_model = user_serializer.load(user_dictionary)
        db.session.add(user_model)
        db.session.commit()
        

        return user_serializer.jsonify(user_model), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"error": e.messages,}),HTTPStatus.BAD_REQUEST,
    except Exception as e:
        return jsonify({"error": "Something went wrong"}), HTTPStatus.INTERNAL_SERVER_ERROR

@router.route("/login", methods=["POST"])
def login():
    credentials = request.json
    username = credentials.get("username")
    password = credentials.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), HTTPStatus.BAD_REQUEST

    user = (
        db.session.query(UserModel)
        .filter_by(username=username)
        .first()
    )

    if not user:
        return jsonify({"error": "Invalid username or password"}), HTTPStatus.UNAUTHORIZED

    if not user.validate_password(password):
        return jsonify({"error": "Invalid username or password"}), HTTPStatus.UNAUTHORIZED

    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(days=1),
        "iat": datetime.now(timezone.utc),
        "sub": user.id,
    }

    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return jsonify({"message": "Login successful.", "token": token}),HTTPStatus.OK

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


@router.route("/all_users", methods=["GET"])
def get_all_user():
    users = db.session.query(UserModel).all()
    print(user_serializer.jsonify(users, many=True))
    return user_serializer.jsonify(users, many=True)


@router.route("/user/<int:user_id>", methods=["DELETE"])
@secure_route
def delete_user(user_id):
    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"message": "user not found"}, HTTPStatus.NOT_FOUND)

    user.remove()
    return jsonify({"error": "user deleted"})
