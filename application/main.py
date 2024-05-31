from .database import db
from flask import jsonify,request,Flask
from flask_restful import reqparse,request,fields,Resource,abort,marshal_with
from .models import Task,User
from flask_jwt_extended.view_decorators import jwt_required
from .limitator import limitater

app = Flask(__name__)

resource_fields = {
    "id":fields.Integer,
    "task":fields.String,
    "summary":fields.String
}

task_create_args = reqparse.RequestParser()
task_create_args.add_argument("task",type=str,help="Task fields is required",required=True)
task_create_args.add_argument("summary",type=str,help="summary fields is required",required=True)


task_put_args = reqparse.RequestParser()
task_put_args.add_argument("task",type=str)
task_put_args.add_argument("summary",type=str)

class ListAllTask(Resource):
    @limitater.limit("3 per minute")
    def get(self):
        tasks = Task.query.all()
        print(tasks)
        all_tasks = {}
        for task in tasks:
            all_tasks[task.id] = {"title":task.task,"summary":task.summary}
        return all_tasks

class TaskDispatch(Resource):
    @jwt_required()
    @marshal_with(resource_fields)
    def get(self,task_id):
        task = Task.query.filter_by(id=task_id).first()
        if not task:    
            abort(404,message="Task is not exists.......")
        return task
    
    @marshal_with(resource_fields)
    @jwt_required()
    def post(self,task_id):
        args = task_create_args.parse_args()
        task = Task.query.filter_by(id=task_id).first()
        if task:
            abort(409,message="Task already exists.....")
        else:
            new_task = Task(task=args["task"],summary=args["summary"])
            db.session.add(new_task)
            db.session.commit()
            return new_task
        
    @marshal_with(resource_fields)
    @jwt_required()
    def put(self,task_id):
        args = task_put_args.parse_args()
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            abort(404,message="Task is not exists")
        else:
            if args["task"]:
                task.task = args["task"]
            if args["summary"]:
                task.summary = args["summary"]
            db.session.commit()
            return task
        
    @jwt_required()
    def delete(self,task_id):
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            abort(404,message="Task is does not exists so deletion is not possible....")
        else:
            db.session.delete(task)
            db.session.commit()
        return jsonify({"message":"Task is deleted successfully..."})
    


