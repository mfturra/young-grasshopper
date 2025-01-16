from marshmallow import Schema, fields

class DegreeSchema(Schema):
    id =        fields.Str(dump_only=True)
    track =     fields.Str(required=True)
    name =      fields.Str(required=True)
    inst_id =   fields.Str(required=True)
    inst_cost = fields.Float(required=True)

class DegreeUpdateSchema(Schema):
    id =        fields.Str(dump_only=True)
    track =     fields.Str()
    name =      fields.Str(required=True)
    inst_id =   fields.Str(required=True)
    inst_cost = fields.Float(required=True)

class InstitutionSchema(Schema):
    id =            fields.Str(dump_only=True)
    inst_type =     fields.Str(required=True)
    inst_name =     fields.Str(required=True)
    inst_cost =     fields.Float(required=True)
    welcome_text = fields.Str(required=True)

class InstitutionUpdateSchema(Schema):
    id =            fields.Str(dump_only=True)
    inst_type =     fields.Str(required=True)
    inst_name =     fields.Str(required=True)
    inst_cost =     fields.Float(required=True)
    welcome_text =  fields.Str(required=True)