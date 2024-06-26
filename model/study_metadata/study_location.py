import datetime
import uuid
from datetime import timezone

from model import Study

from ..db import db


class StudyLocation(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "study_location"

    id = db.Column(db.CHAR(36), primary_key=True)
    facility = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    zip = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)

    study_id = db.Column(
        db.CHAR(36), db.ForeignKey("study.id", ondelete="CASCADE"), nullable=False
    )
    study_location_contact_list = db.relationship(
        "StudyLocationContactList",
        back_populates="study_location",
        cascade="all, delete",
    )
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
            "created_at": self.created_at,
        }

    def to_dict_metadata(self):
        """Converts the study metadata to a dictionary"""
        return {
            "id": self.id,
            "facility": self.facility,
            "country": self.country,
        }

    @staticmethod
    def from_data(study: Study, data: dict):
        """Creates a new study from a dictionary"""
        study_location = StudyLocation(study)
        study_location.update(data)

        return study_location

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        self.facility = data["facility"]
        self.status = data["status"]
        self.city = data["city"]
        self.state = data["state"]
        self.zip = data["zip"]
        self.country = data["country"]
        self.study.touch()

    def validate(self):
        """Validates the lead_sponsor_last_name study"""
        violations: list = []
        return violations
