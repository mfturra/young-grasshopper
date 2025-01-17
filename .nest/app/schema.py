from marshmallow import Schema, fields

class PlainDegreeSchema(Schema):
    id =        fields.Str(dump_only=True)
    track =     fields.Str(required=True)
    name =      fields.Str(required=True)

class PlainInstitutionSchema(Schema):
    id =            fields.Str(dump_only=True)
    inst_type =     fields.Str(required=True)
    inst_name =     fields.Str(required=True)
    inst_cost =     fields.Float(required=True)
    welcome_text =  fields.Str(required=True)

class DegreeUpdateSchema(Schema):
    id =        fields.Str(dump_only=True)
    track =     fields.Str()
    name =      fields.Str(required=True)
    desc =      fields.Str(required=True)

class DegreeSchema(PlainDegreeSchema):
   inst_id      = fields.Int(required=True, load_only=True)
   inst_cost    = fields.Float(required=True, load_only=True)
   institution  = fields.Nested(PlainInstitutionSchema(), dump_only=True)

class InstitutionSchema(PlainInstitutionSchema):
    degrees = fields.List(fields.Nested(PlainDegreeSchema), dump_only=True)

    # id =            fields.Str(dump_only=True)
    # inst_type =     fields.Str(required=True)
    # inst_name =     fields.Str(required=True)
    # inst_cost =     fields.Float(required=True)
    # welcome_text =  fields.Str(required=True)