import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import degrees
from schema import DegreeSchema, DegreeUpdateSchema

blp = Blueprint("degrees", __name__, description="Operations on degrees")

@blp.route('/degrees/<string:degree_id>')
class Degree(MethodView):
    @blp.response(200, DegreeSchema)
    def get(self, degree_id):
        try:
            return degrees[degree_id]
        except KeyError:
            abort(404, message="Degree was not found.")
    
    def delete(self, degree_id):
        try:
            del degrees[degree_id]
        except KeyError:
            abort(404, message="Degree was not found.")

    # check if payload includes all elements
    @blp.arguments(DegreeUpdateSchema)
    
    # config success response type
    @blp.response(200, DegreeUpdateSchema)
    def put(self, degree_data, degree_id):
        try:
            degree = degrees[degree_id]
            degree |= degree_data # merge dictionary
            return degree, 201
        except KeyError:
            abort(404, message="Institution was not found.")

@blp.route("/degrees")
class DegreeList(MethodView):
    # config success response type
    @blp.response(200, DegreeSchema)
    def get(self):
        return degrees.values()
    
    # check if payload includes all elements
    @blp.arguments(DegreeSchema)
    
    # config success response type
    @blp.response(201, DegreeSchema)
    def post(self, degree_data):        
        # check for duplicate degree entries
        for degree in degrees.values():
            if (
                degree_data["degree_name"] == degree["degree_name"]
                and degree_data["degree_track"] == degree["degree_track"]
                and degree_data["inst_id"] == degree["inst_id"]
            ):
                abort(
                    404,
                    message="Degree has already been created."
                    )
                
        degree_id = uuid.uuid4().hex
        degree = {**degree_data, "id": degree_id}
        degrees[degree_id] = degree
        return degree, 201