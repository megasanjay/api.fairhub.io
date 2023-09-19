import uuid
from datetime import datetime
from .db import db
from datetime import timezone
import datetime
import app


class User(db.Model):
    def __init__(self, password, data):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()
        self.set_password(password, data)

    __tablename__ = "user"
    id = db.Column(db.CHAR(36), primary_key=True)
    email_address = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    orcid = db.Column(db.String, nullable=False)
    hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    institution = db.Column(db.String, nullable=False)
    study_contributors = db.relationship("StudyContributor", back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "email_address": self.email_address,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "orcid": self.orcid,
            "created_at": self.created_at,
            "institution": self.institution,
        }

    @staticmethod
    def from_data(data: dict):
        user = User(data["password"], data)
        user.update(data)
        return user

    def update(self, data):
        self.email_address = data["email_address"]
        self.username = data["username"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.orcid = data["orcid"]
        self.institution = data["institution"]

    def set_password(self, password, data):
        hashed_password = app.bcrypt.generate_password_hash(password).decode("utf-8")
        self.hash = hashed_password

    def check_password(self, password):
        hashed_password = app.bcrypt.generate_password_hash(password).decode("utf-8")
        is_valid = app.bcrypt.check_password_hash(hashed_password, password)
        return is_valid
