from db import db
from datetime import datetime
from typing import List

from models.execution_result import ExecutionResultModel


class TestCaseModel(db.Model):
    __tablename__ = "test_cases"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship("UserModel", back_populates="test_cases")

    @classmethod
    def find_by_id(cls, _id: int) -> "TestCaseModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_user_by_id(cls, user_id: int):
        return cls.query.filter_by(user_id=user_id).first()

    # return List
    @classmethod
    def find_all(cls) -> List["TestCaseModel"]:
        return cls.query.all()

    # insert data
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # delete data
    def delete_from_db(self):
        ExecutionResultModel.query.filter_by(test_case_id=self.id).delete()
        db.session.delete(self)
        db.session.commit()
