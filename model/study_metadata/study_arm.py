import datetime
import uuid
from datetime import timezone

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY

import model

from ..db import db


class StudyArm(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "study_arm"

    id = db.Column(db.CHAR(36), primary_key=True)
    label = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=False)
    intervention_list = db.Column(ARRAY(String), nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)

    study_id = db.Column(
        db.CHAR(36), db.ForeignKey("study.id", ondelete="CASCADE"), nullable=False
    )
    study = db.relationship("Study", back_populates="study_arm")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "label": self.label,
            "type": self.type,
            "description": str(self.description),
            "intervention_list": self.intervention_list,
            "created_at": self.created_at,
        }

    def to_dict_metadata(self):
        """Converts the study metadata to a dictionary"""
        return {
            "id": self.id,
            "label": self.label,
            "description": self.description,
        }

    @staticmethod
    def from_data(study: model.Study, data: dict):
        """Creates a new study from a dictionary"""
        study_arm = StudyArm(study)
        study_arm.update(data)
        return study_arm

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        self.label = data["label"]
        self.type = data["type"]
        self.description = data["description"]
        self.intervention_list = data["intervention_list"]
        self.study.touch()

    def validate(self):
        """Validates the study"""
        violations: list = []
        return violations
