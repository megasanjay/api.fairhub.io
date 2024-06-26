import datetime
import uuid
from datetime import timezone

from ..db import db


class DatasetContributorAffiliation(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "dataset_contributor_affiliation"
    id = db.Column(db.CHAR(36), primary_key=True)
    identifier = db.Column(db.String, nullable=False)
    identifier_scheme = db.Column(db.String, nullable=False)
    identifier_scheme_uri = db.Column(db.String, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)

    # dataset_contributors = db.relationship(
    #     "DatasetContributor", back_populates="dataset_contributor_affiliation"
    # )
    contributor_id = db.Column(
        db.String, db.ForeignKey("dataset_contributor.id"), nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "identifier": self.identifier,
            "identifier_scheme": self.identifier_scheme,
            "identifier_scheme_uri": self.identifier_scheme_uri,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_contributor = DatasetContributorAffiliation(dataset)
        dataset_contributor.update(data)
        return dataset_contributor

    def update(self, data: dict):
        self.identifier = data["identifier"]
        self.identifier_scheme = data["identifier_scheme"]
        self.identifier_scheme_uri = data["identifier_scheme_uri"]
        self.dataset.touch_dataset()
