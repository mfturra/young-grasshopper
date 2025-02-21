import os
from dotenv import load_dotenv

from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

from db import db
import models

from resources.institution import blp as InstitutionBlueprint
from resources.degree import blp as DegreeBlueprint

load_dotenv()

# database credentials
user =      os.environ.get('DB_USER')
password =  os.environ.get('DB_PASSWORD')
host =      os.environ.get('DB_HOST')
port =      os.environ.get('DB_PORT')
database =  os.environ.get('DB_DATABASE')
DB_URL = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
    user, password, host, port, database
    )



def create_app(db_url=None):
    # initialize app
    app = Flask(__name__) 
    print("Initializing Flask app")

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Young Grasshopper REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app) # initialize the Flask SQLAlchemy extension 
    print("Initialized SQLAlchemy")

    # class InstitutionModel(db.Model):
    #     __tablename__ = "institutions"

    #     id =            db.Column(db.Integer, primary_key=True)
    #     inst_type =     db.Column(db.String(30), unique=True, nullable=False)
    #     uni_name =      db.Column(db.String(30), unique=True, nullable=False)
    #     uni_type =      db.Column(db.String(25), unique=True, nullable=False)
    #     uni_welcome =   db.Column(db.String(300), unique=True, nullable=False)
    #     uni_cost =      db.Column(db.Float(precision=2), unique=False, nullable=False)
    #     degree =        db.relationship("DegreeModel", back_populates="degree", lazy="dynamic")
    
    # class DegreeModel(db.Model):
    #     __tablename__ = "degrees"

    #     # "unique=True" = Not duplicates
    #     id =                        db.Column(db.Integer, primary_key=True)
    #     degree_track =              db.Column(db.String(30), unique=True, nullable=False)
    #     degree_name =               db.Column(db.String(30), unique=True, nullable=False)
    #     degree_desc =               db.Column(db.String(500), unique=True, nullable=False)
    #     curriculum_difficulty =     db.Column(db.Float(precision=2), unique=False, nullable=False)
    #     uni_id =                    db.Column(db.Integer, db.ForeignKey("institutions.id"), unique=False, nullable=False)
    #     degrees =                   db.relationship("InstitutionModel", back_populates="institution", lazy="dynamic")

    api = Api(app)

    with app.app_context():
        print("Creating database tables.")
        db.create_all()
        print("Database tables created.")

    api.register_blueprint(DegreeBlueprint)
    api.register_blueprint(InstitutionBlueprint)

    return app