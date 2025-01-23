import uuid
# from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import DegreeModel
from schema import DegreeSchema, DegreeUpdateSchema

blp = Blueprint("degree", __name__, description="Operations on degrees")

@blp.route('/degrees/<string:degree_id>')
class Degree(MethodView):
    @blp.response(200, DegreeSchema)
    def get(self, degree_id):
        degree = DegreeModel.query.get_or_404(degree_id)
        return degree
    
    def delete(self, degree_id):
        degree = DegreeModel.query.get_or_404(degree_id)
        raise NotImplementedError("Deleting not yet implemented.")

    # check if payload includes all elements
    @blp.arguments(DegreeUpdateSchema)
    
    # config success response type
    @blp.response(200, DegreeUpdateSchema)
    def put(self, degree_data, degree_id):
        degree = DegreeModel.query.get_or_404(degree_id)
        raise NotImplementedError("Deleting not yet implemented.")

@blp.route("/degrees")
class DegreeList(MethodView):
    # config success response type
    @blp.response(200, DegreeSchema)
    def get(self):
        return #degrees.values()
    
    # check if payload includes all elements
    @blp.arguments(DegreeSchema)
    
    # config success response type
    @blp.response(201, DegreeSchema)
    def post(self, degree_data):        
        degree = DegreeModel(**degree_data)

        try:
            db.session.add(degree)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occurred when inserting the item.")

        return degree