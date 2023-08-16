import uuid
from datetime import datetime
from .db import db


class StudyInvitedContributor(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "invited_study_contributor"
    email_address = db.Column(db.String, nullable=False, primary_key=True)
    permission = db.Column(db.String, nullable=False)
    invited_on = db.Column(db.DateTime, nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"), primary_key=True)
    study = db.relationship("Study", back_populates="invited_contributors")

    def to_dict(self):
        return {
            "email_address": self.id,
            "permission": self.permission,
            "invited_on": datetime.now(),
        }

    @staticmethod
    def from_data(data: dict):
        invited_contributor = StudyInvitedContributor()
        invited_contributor.email_address = data["email_address"]
        invited_contributor.permission = data["permission"]
        invited_contributor.invited_on = data["invited_on"]

        return invited_contributor