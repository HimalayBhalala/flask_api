# from flask import Flask,jsonify,request
# from flask_restful import Api,Resource,reqparse,abort,fields,marshal_with
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask import Flask

# app = Flask(__name__,instance_relative_config=True)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

# api = Api(app)

# db = SQLAlchemy(app)
# migrate = Migrate(app,db)

# class Task(db.Model):
#     id = db.Column(db.Integer,primary_key=True,unique=True,autoincrement=True)
#     task = db.Column(db.String(100),nullable=False)
#     summary = db.Column(db.String(100),nullable=False) 

# with app.app_context():
#     db.create_all()

# resource_fields = {
#     "id":fields.Integer,
#     "title":fields.String,
#     "post":fields.String
# }

# tasks = {
#     1:{"task":"swap two number","summary":"Swap two number without use of third variable"},
#     2:{"task":"add two number","summary":"Give sum of two number"},
#     3:{"task":"print average of two number","summary":"Give average of a two number"}
# }

# task_post_args = reqparse.RequestParser()
# task_post_args.add_argument("task",type=str,help="Task is required",required=True)
# task_post_args.add_argument("summary",type=str,help="Summary is required",required=True)

# task_put_args = reqparse.RequestParser()
# task_put_args.add_argument("task",type=str)
# task_put_args.add_argument("summary",type=str)

# all_task = {}

# class GetAll(Resource):
#     def get(self):
#         tasks = Task.query.all()
#         all_task = {}
#         for task in tasks:
#             all_task[task.id] = {"task":task.task,"summary":task.summary}
#         return all_task
    
# class GetOne(Resource):
#     def get(self,task_id):
#         task = Task.query.filter_by(id=task_id).first()
#         if task:
#             task[task_id] = {"title":task.title,"summary":task.summary}
#             return task
#         else:
#             abort(404,message="Task id is not exists.")
        
#     @marshal_with(resource_fields)
#     def post(self,task_id):
#         args = task_post_args.parse_args()

        
    
    # @marshal_with(resource_fields)
    # def put(self,task_id):
    #     args = task_put_args.parse_args()

    #     if task_id in tasks:
    #         if args["task"]:
    #             tasks[task_id]["task"] = args["task"]
    #         if args["summary"]:
    #             tasks[task_id]["summary"] = args["summary"]
    #         return tasks[task_id]
    #     else:
    #         abort(404,message="Task is not exists")

    # @marshal_with(resource_fields)
    # def delete(self,task_id):
    #     if task_id in tasks:
    #         del tasks[task_id]
    #         return jsonify({"message":"Task is deleted successfully","status":True})
    #     else:
    #         abort(404,message="Task is not exists so can not delete it.")

# api.add_resource(GetAll,"/helo/")
# api.add_resource(GetOne,"/helo/<int:task_id>/")