from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY

from ..db import db


class DatasetOther(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.dataset = dataset
        self.resource_type = ""
        self.language = None
        self.size = ""
        self.format = ""
        self.standards_followed = ""
        self.acknowledgement = ""

    __tablename__ = "dataset_other"

    resource_type = db.Column(db.String, nullable=False)
    language = db.Column(db.String, nullable=True)
    size = db.Column(ARRAY(String), nullable=False)
    format = db.Column(ARRAY(String), nullable=False)
    standards_followed = db.Column(db.String, nullable=False)
    acknowledgement = db.Column(db.String, nullable=False)

    dataset_id = db.Column(
        db.CHAR(36), db.ForeignKey("dataset.id"), primary_key=True, nullable=False
    )
    dataset = db.relationship("Dataset", back_populates="dataset_other")

    def to_dict(self):
        return {
            "language": self.language,
            "standards_followed": self.standards_followed,
            "acknowledgement": self.acknowledgement,
            "size": self.size,
            "format": self.format,
            "resource_type": self.resource_type,
        }

    def to_dict_metadata(self):
        return {
            "language": self.language,
            "size": self.size,
            "resource_type": self.resource_type,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_other = DatasetOther(dataset)
        dataset_other.update(data)
        return dataset_other

    def update(self, data: dict):
        if "language" in data:
            self.language = data["language"]
        if "size" in data:
            self.size = data["size"]
        if "format" in data:
            self.format = data["format"]
        if "acknowledgement" in data:
            self.acknowledgement = data["acknowledgement"]
        if "standards_followed" in data:
            self.standards_followed = data["standards_followed"]
        if "resource_type" in data:
            self.resource_type = data["resource_type"]
        self.dataset.touch_dataset()
