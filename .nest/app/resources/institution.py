from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import InstitutionModel
from schema import InstitutionSchema, InstitutionUpdateSchema

from db import db

blp = Blueprint("institution", __name__, description="Operations on institutions")

@blp.route("/institutions/<string:inst_id>")
class Institution(MethodView):
    # config success response type
    @blp.response(200, InstitutionSchema)
    def get(self, inst_id):
        institution = InstitutionModel.query.get_or_404(inst_id)
        return institution

    def delete(self, inst_id):
        institution = InstitutionModel.query.get_or_404(inst_id)
        raise NotImplementedError("Delete not yet implemented.")
    

    # check if payload includes all elements
    @blp.arguments(InstitutionUpdateSchema)
    
    # config success response type
    @blp.response(200, InstitutionUpdateSchema)
    def put(self, inst_data, inst_id):
        institution = InstitutionModel.query.get_or_404(inst_id)
        raise NotImplementedError("Update not yet implemented.")
        
@blp.route("/institutions")
class InstitutionList(MethodView):
    @blp.response(200, InstitutionSchema(many=True))
    def get(self):
        # institution = InstitutionModel(**inst_data)
        return #db.values()
    
    # check if payload includes all elements
    @blp.arguments(InstitutionSchema)

    # config success response type
    @blp.response(201, InstitutionSchema)
    def post(self, inst_data):
        institution = InstitutionModel(**inst_data)
        try:
            db.session.add(institution)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="Institution with name already exists."
            )
        except SQLAlchemyError:
            abort(
                500,
                message="Error occurred when creating institution."
            )

        # future iteration: route admin to webpage of new institution created
        return