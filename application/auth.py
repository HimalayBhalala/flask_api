from flask import Blueprint,jsonify,request
from .models import User,TokenBlackListModel
from .database import db
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt,jwt_required

auth = Blueprint('auth',__name__)

@auth.post("/register")
def register():
    data = request.get_json()
    user = User.get_user_by_email(email=data.get("email"))
    if user is not None:
        return jsonify({"error":"Email is already exists."})
    else:
        new_user = User(first_name=data.get("first_name"),last_name=data.get("last_name"),email=data.get("email"),password=data.get("password"))
        new_user.save()
        return jsonify({"data":
                        {"id":new_user.id,
                        "first_name":new_user.first_name,"last_name":new_user.last_name,
                        "email":new_user.email
                        }
                       }),201

@auth.post("/login")
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()
    if user is None:
        return jsonify({"error":"User is not register."})
    if user and user.check_password(data.get("password")):
        access_token = create_access_token(identity=user.email)
        refresh_token = create_refresh_token(identity=user.email)

        return jsonify({"response":
                        {"status":"User Logged in success","token":{"access_token":access_token,"refresh_token":refresh_token}}})
    return jsonify({"error":"Invalid email and password"})


@auth.post("/logout")
@jwt_required()
def logout():
    claim = get_jwt()
    jti = claim["jti"]
    print(jti)
    token_block = TokenBlackListModel(jti=jti)

    token_block.save()

    return jsonify({"message":"Logout SuccessFully...."})