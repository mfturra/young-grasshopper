import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import institutions
from schema import InstitutionSchema, InstitutionUpdateSchema

blp = Blueprint("institutions", __name__, description="Operations on institutions")

@blp.route("/institutions/<string:inst_id>")
class Institution(MethodView):
    # config success response type
    @blp.response(200, InstitutionSchema)
    def get(self, inst_id):
        try:
            # future iteration: route user to webpage of welcome banner of institution
            return institutions[inst_id]
        except KeyError:
            return { "message":"Institution not found."}, 404

    def delete(self, inst_id):
        try:
            del institutions[inst_id]
            return {"message": "Institution successfully deleted."}
        except KeyError:
            return {"message": "Institution not found."}
    
    

    # check if payload includes all elements
    @blp.arguments(InstitutionUpdateSchema)
    
    # config success response type
    @blp.response(200, InstitutionUpdateSchema)
    def put(self, inst_data, inst_id):
        try:
            inst = institutions[inst_id]
            inst |= inst_data # merge dictionary
            return inst, 201
        except KeyError:
            abort(404, message="Institution was not found.")
        
@blp.route("/institutions")
class InstitutionList(MethodView):
    @blp.response(200, InstitutionSchema(many=True))
    def get(self):
        return institutions.values()
    
    # check if payload includes all elements
    @blp.arguments(InstitutionSchema)

    # config success response type
    @blp.response(201, InstitutionSchema)
    def post(self, inst_data):
        for inst in institutions.values():
            if (
                inst_data["inst_type"] == inst["inst_type"]
                and inst_data["inst_name"] == inst["inst_name"]
                and inst_data["inst_cost"] == inst["inst_cost"]
            ):
                abort(
                    404,
                    message="Institution already exists.")

        # create institution
        inst_id = uuid.uuid4().hex

        inst = {**inst_data, "inst_id": inst_id, "name": "inst_name"}
        institutions[inst_id] = inst

        # future iteration: route admin to webpage of new institution created
        return inst, 201