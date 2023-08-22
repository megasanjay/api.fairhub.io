import uuid
from ..db import db

class StudyLocation(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "study_location"

    id = db.Column(db.CHAR(36), primary_key=True)
    facility = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    zip = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="study_location")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "facility": self.facility,
            "status": self.status,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "country": self.country,
        }

    @staticmethod
    def from_data(data: dict):
        """Creates a new study from a dictionary"""
        study_location = StudyLocation()
        study_location.update(data)

        return study_location

    def update(self, data):
        """Updates the study from a dictionary"""
        self.facility = data["facility"]
        self.status = data["status"]
        self.city = data["city"]
        self.state = data["state"]
        self.zip = data["zip"]
        self.country = data["country"]

    def validate(self):
        """Validates the lead_sponsor_last_name study"""
        violations = []
        return violations