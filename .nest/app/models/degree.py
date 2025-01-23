from db import db

class DegreeModel(db.Model):
    __tablename__ = "Degrees"

    # "unique=True" = Not duplicates
    id =                        db.Column(db.Integer, primary_key=True)
    degree_track =              db.Column(db.String(30), unique=True, nullable=False)
    degree_name =               db.Column(db.String(30), unique=True, nullable=False)
    degree_desc =               db.Column(db.String(500), unique=True, nullable=False)
    curriculum_difficulty =     db.Column(db.Float(precision=2), unique=False, nullable=False)
    uni_id =                    db.Column(db.Integer, db.ForeignKey("institutions.id"), unique=False, nullable=False)
    degrees =                   db.relationship("InstitutionModel", back_populates="institution", lazy="dynamic")