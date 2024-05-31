from .database import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    first_name = db.Column(db.String(200),nullable=False)
    last_name = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),unique=True,nullable=False)
    password = db.Column(db.String(100),nullable=False)
    created = db.Column(db.DateTime)
    
    def __init__(self,first_name,last_name,email,password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.created = datetime.now()

    def check_password(self,password):
        return check_password_hash(self.password,password)
    
    @classmethod
    def get_user_by_email(cls,email):
        return cls.query.filter(cls.email==email).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    task = db.Column(db.String(100),nullable=False)
    summary = db.Column(db.String(200),nullable=False)

class TokenBlackListModel(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    jti = db.Column(db.String(200),nullable=False)
    created_on = db.Column(db.DateTime,default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"Token id is: {self.jti}"

