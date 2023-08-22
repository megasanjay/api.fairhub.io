import uuid

from ..db import db


class StudyStatus(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self):
        self.id = str(uuid.uuid4())
        # self.created_at = datetime.now()

    __tablename__ = "study_status"

    id = db.Column(db.CHAR(36), primary_key=True)
    overall_status = db.Column(db.String, nullable=False)
    why_stopped = db.Column(db.String, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    start_date_type = db.Column(db.String, nullable=False)
    completion_date = db.Column(db.DateTime, nullable=False)
    completion_date_type = db.Column(db.String, nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="study_status")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "overall_status": self.overall_status,
            "why_stopped": self.why_stopped,
            "start_date": str(self.start_date),
            "start_date_type": self.start_date_type,
            "completion_date": str(self.completion_date),
            "completion_date_type": self.completion_date_type,

        }

    @staticmethod
    def from_data(data: dict):
        """Creates a new study from a dictionary"""
        study_status = StudyStatus()
        study_status.update(data)

        return study_status

    def update(self, data):
        """Updates the study from a dictionary"""
        self.overall_status = data["title"]
        self.why_stopped = data["image"]
        self.start_date = data["created_at"]
        self.start_date_type = data["updated_on"]
        self.completion_date = data["title"]
        self.completion_date_type = data["image"]

    def validate(self):
        """Validates the study"""
        violations = []
        return violations