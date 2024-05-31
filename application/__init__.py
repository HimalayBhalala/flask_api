from decouple import config
from flask import Flask,jsonify,request
from flask_restful import Api
from .main import ListAllTask,TaskDispatch
from .auth import auth as auth_bp
from .user import user as user_bp
from .models import User,TokenBlackListModel
from .database import db,jwt
from .limitator import limitater
from flask_limiter.util import get_remote_address

def create_app():

    app = Flask(__name__,instance_relative_config=True)

    app.config["SQLALCHEMY_DATABASE_URI"]=config("SQLALCHEMY_DATABASE_URI")

    app.config.from_prefixed_env()
    
    db.init_app(app)
    jwt.init_app(app)
    limitater.init_app(app)

    with app.app_context():
        db.create_all()

    api = Api(app)

    api.add_resource(ListAllTask,'/all')
    api.add_resource(TaskDispatch,'/task/<string:task_id>/')

    @app.route('/')
    def hello():
        return '<h1>Hello</h1>'

    app.register_blueprint(auth_bp,url_prefix='/auth')
    app.register_blueprint(user_bp,url_prefix="/user")

    #load user

    @jwt.user_lookup_loader
    def user_lookup(jwt_header,jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(email = identity).one_or_none()

    # add jwt error handler

    @jwt.expired_token_loader
    def token_has_been_expired(jwtheader,jwtdata):
        return jsonify({"message":"Token has bin expired","error":"Token is Expired"}),401
    
    @jwt.invalid_token_loader
    def token_has_been_invalid(error):
        return jsonify({"message":"Signature of token has been invalid","error":"Invalid Signature"}),401
    
    @jwt.unauthorized_loader
    def token_has_been_unauthenticated(error):
        return jsonify({"message":"Token has been unauthenticated","error":"Token is not set"}),401

    #Add additional claim

    @jwt.additional_claims_loader
    def add_additional_information_in_claim(identity):
        if identity == "hanuman@gmail.com":
            return {"is_staff":True}
        return {"is_staff":False}
    
    @jwt.token_in_blocklist_loader
    def token_in_block_list(jwt_header,jwt_data):
        jti = jwt_data["jti"]
        token = db.session.query(TokenBlackListModel).filter(TokenBlackListModel.jti==jti).scalar()
        return token
    
    @app.get("/search")
    def search_fun():
        search = request.args.get("q")
        response = User.query.filter_by(email=search).first()
        print(response)
        if response:
            return jsonify({"first_name":response.first_name,"last_name":response.last_name,"created":response.created})
        else:
            return jsonify({"error":"No data found"}),404

    # app.testing = True
    # client = app.test_client()

    # with app.test_client() as c:
    #     response = c.get('/task/?task_id=3')
    #     assert request.args['task_id'] == '3'

    return app
