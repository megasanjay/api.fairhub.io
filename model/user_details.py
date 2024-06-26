import uuid

import model

from .db import db


class UserDetails(db.Model):  # type: ignore
    def __init__(self, user):
        self.id = str(uuid.uuid4())
        self.first_name = ""
        self.last_name = ""
        self.institution = ""
        self.location = ""
        self.timezone = ""
        self.orcid = ""
        self.profile_image = ""
        self.user = user

    __tablename__ = "user_details"
    id = db.Column(db.CHAR(36), primary_key=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    institution = db.Column(db.String, nullable=True)
    orcid = db.Column(db.String, nullable=True)
    location = db.Column(db.String, nullable=True)
    profile_image = db.Column(db.String, nullable=True)

    timezone = db.Column(db.String, nullable=True)
    user_id = db.Column(db.CHAR(36), db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="user_details")

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "institution": self.institution,
            "orcid": self.orcid,
            "location": self.location,
            "timezone": self.timezone,
            "profile_image": self.profile_image,
        }

    @staticmethod
    def from_data(user: model.User, data: dict):
        user = UserDetails(user)
        user.update(data)
        return user

    def update(self, data: dict):
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.institution = data["institution"]
        self.orcid = data["orcid"]
        self.location = data["location"]
        self.timezone = data["timezone"]
        self.profile_image = data["profile_image"] if "profile_image" in data else ""
