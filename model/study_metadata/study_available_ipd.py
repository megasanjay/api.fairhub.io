import uuid

from ..db import db


class StudyAvailableIpd(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self):
        self.id = str(uuid.uuid4())
    __tablename__ = "study_available_ipd"

    id = db.Column(db.CHAR(36), primary_key=True)
    identifier = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="study_available_ipd")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "identifier": self.identifier,
            "type": self.type,
            "url": self.url,
            "comment": self.comment,
        }

    @staticmethod
    def from_data(data: dict):
        """Creates a new study from a dictionary"""
        study_available = StudyAvailableIpd()
        study_available.update(data)
        return study_available

    def update(self, data):
        """Updates the study from a dictionary"""
        self.identifier = data["identifier"]
        self.type = data["type"]
        self.url = data["url"]
        self.comment = data["comment"]

    def validate(self):
        """Validates the study"""
        violations = []
        return violations