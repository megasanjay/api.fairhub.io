import uuid

from ..db import db


class DatasetRelatedItem(db.Model):
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset

    __tablename__ = "dataset_related_item"
    id = db.Column(db.CHAR(36), primary_key=True)
    type = db.Column(db.String, nullable=False)
    relation_type = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_related_item")
    dataset_related_item_contributor = db.relationship(
        "DatasetRelatedItemContributor", back_populates="dataset_related_item"
    )
    dataset_related_item_identifier = db.relationship(
        "DatasetRelatedItemIdentifier", back_populates="dataset_related_item"
    )
    dataset_related_item_other = db.relationship(
        "DatasetRelatedItemOther", back_populates="dataset_related_item"
    )
    dataset_related_item_title = db.relationship(
        "DatasetRelatedItemTitle", back_populates="dataset_related_item"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "relation_type": self.relation_type,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_related_item = DatasetRelatedItem(dataset)
        dataset_related_item.update(data)
        return dataset_related_item

    def update(self, data):
        self.type = data["type"]
        self.relation_type = data["relation_type"]
