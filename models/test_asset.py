from typing import List
from db import db


class TestAssetModel(db.Model):
    __tablename__ = "test_assets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    @classmethod
    def find_by_id(cls, _id: int) -> "TestAssetModel":
        return cls.query.filter_by(id=_id).first()

    # return List
    @classmethod
    def find_all(cls) -> List["TestAssetModel"]:
        return cls.query.all()

    # insert data
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # delete data
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
