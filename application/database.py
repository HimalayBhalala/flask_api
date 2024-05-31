from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS "] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)
jwt = JWTManager()

with app.app_context():
    db.create_all()