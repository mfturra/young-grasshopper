from db import db

class InstitutionModel(db.Model):
    __tablename__ = "institutions"

    id =            db.Column(db.Integer, primary_key=True)
    inst_type =     db.Column(db.String(30), unique=True, nullable=False)
    uni_name =      db.Column(db.String(30), unique=True, nullable=False)
    uni_type =      db.Column(db.String(25), unique=True, nullable=False)
    uni_welcome =   db.Column(db.String(300), unique=True, nullable=False)
    uni_cost =      db.Column(db.Float(precision=2), unique=False, nullable=False)
    degree =        db.relationship("DegreeModel", back_populates="degree", lazy="dynamic")
    # degree_id =     db.Column(db.Integer, db.ForeignKey("degrees.id"), unique=False, nullable=False)
    # curriculum_id = db.Column(db.Integer, db.ForeignKey('curriculum.id'), unique=False, nullable=False)