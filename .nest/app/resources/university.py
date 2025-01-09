import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from prelim_db import institutions

blp = Blueprint("institutions", __name__, description="Operations on institutions")

@blp.route("/<string:inst_id>")
class Institution(MethodView):
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
        
@blp.route("/")
class InstitutionList(MethodView):
    def get(self):
        return {"institutions": list(institutions.values())}
    
    def post(self):
        inst_data = request.get_json()

        # check if payload includes an inst_name
        if "inst_name" not in inst_data:
            abort(404, message="Ensure that 'inst_name' is included in JSON payload.")
        
        # check if institution already exists
        for institution in institutions.values():
            if inst_data["inst_name"] == institution["inst_name"]:
                return { "message":"Institution already exists."}, 403 #abort(400, message="Bad request. The institution that you requested already exists.")

        # create institution
        inst_id = uuid.uuid4().hex

        new_inst = {**inst_data, "inst_id": inst_id, "name": "inst_name"}
        institutions[inst_id] = new_inst

        # future iteration: route admin to webpage of new institution created
        return new_inst, 201