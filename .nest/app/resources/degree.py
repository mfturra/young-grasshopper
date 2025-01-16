import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import degrees
from schema import DegreeSchema, DegreeUpdateSchema

blp = Blueprint("degrees", __name__, description="Operations on degrees")

@blp.route('/degrees/<string:degree_id>')
class Degree(MethodView):
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

    @blp.arguments(DegreeUpdateSchema)
    def put(self, degree_data, degree_id):
        try:
            degree = degrees[degree_id]
            degree |= degree_data # merge dictionary
            return degree, 201
        except KeyError:
            abort(404, message="Institution was not found.")

@blp.route("/degrees")
class DegreeList(MethodView):
    def get(self):
        return {"degrees": list(degrees.values())}
    
    # check payload for all required items
    @blp.arguments(DegreeSchema)
    
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