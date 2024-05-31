from flask import Blueprint,jsonify,request
from .models import User
from .schema import UserSchema
from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended import get_jwt,current_user,get_jwt_identity,create_access_token

user = Blueprint("user",__name__)

@user.get("/all")
@jwt_required()
def get_all_user():
    claim = get_jwt()
    if claim["is_staff"] == True:
        page = request.args.get("page",default=1,type=int)
        per_page = request.args.get("per_page",default=3,type=int)

        users = User.query.paginate(
            page = page,
            per_page = per_page,
        )

        result = UserSchema().dump(users,many=True)
        data = {}
        for response in result:
                data[response["id"]] = {"first_name":response["first_name"],"last_name":response["last_name"],"email":response["email"],"created":response["created"]}
        return jsonify({"users":data})
    return jsonify({"message":"You have not able to access all user api it is only show admin."})

@user.get("<int:id>/")
def get_user_by_id(id):
    get_user = User.query.filter_by(id=id).first()

    if not get_user:
        return jsonify({"message":"user is not exists with this id."})

    return jsonify({"data":
                    {
                        "id":id,
                        "user_info":{"first_name":get_user.first_name,"last_name":get_user.last_name,"email":get_user.email}
                    }
                }), 200


@user.get("/token/info")
@jwt_required()
def get_token_claim_info():
     jwt_claim = get_jwt()
     return jsonify({"message":"Information of jwt token","user_detail":{"first_name":current_user.first_name,"last_name":current_user.last_name,"email":current_user.email},"claims":jwt_claim})

@user.get("/token/refresh")
@jwt_required(refresh=True)
def get_refresh_token():
     identity = get_jwt_identity()
     access_token = create_access_token(identity=identity)
     return jsonify({"message":"Access token is created successfully....","access_token":access_token})