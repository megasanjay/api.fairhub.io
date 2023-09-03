import uuid
from ..db import db


class StudyOverallOfficial(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study

    __tablename__ = "study_overall_official"

    id = db.Column(db.CHAR(36), primary_key=True)
    name = db.Column(db.String, nullable=False)
    affiliation = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="study_overall_official")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "affiliation": self.affiliation,
            "role": self.role,
        }

    @staticmethod
    def from_data(study, data: dict):
        """Creates a new study from a dictionary"""
        study_overall_official = StudyOverallOfficial(study)
        study_overall_official.update(data)

        return study_overall_official

    def update(self, data):
        """Updates the study from a dictionary"""
        self.name = data["name"]
        self.affiliation = data["affiliation"]
        self.role = data["role"]

    def validate(self):
        """Validates the study"""
        violations = []
        return violations
