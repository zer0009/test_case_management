from db import db
from typing import List


class ExecutionResultModel(db.Model):
    __tablename__ = "execution_results"

    id = db.Column(db.Integer, primary_key=True)
    test_case_id = db.Column(db.Integer, db.ForeignKey('test_cases.id'), nullable=False)
    test_asset_id = db.Column(db.Integer, db.ForeignKey('test_asset.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    execution_time = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    # Define relationships
    test_case = db.relationship('TestCaseModel', backref=db.backref('execution_results', lazy=True))
    test_asset = db.relationship('TestAssetModel', backref=db.backref('execution_results', lazy=True))

    @classmethod
    def find_by_id(cls, _id: int) -> "ExecutionResultModel":
        return cls.query.filter_by(id=_id).first()

    # return List
    @classmethod
    def find_state_by_id(cls, state_id: int):
        return cls.query.filter_by(state_id=state_id).first()

    @classmethod
    def find_user_by_id(cls, user_id: int):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_user_by_id_all(cls, user_id: int):
        return cls.query.filter_by(user_id=user_id).all()

    # return List
    @classmethod
    def find_all(cls) -> List["ExecutionResultModel"]:
        return cls.query.all()

    # insert data
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # delete data
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
