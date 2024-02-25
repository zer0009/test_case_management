from flask import Flask, jsonify
from flask_restful import Api
from dotenv import load_dotenv
from blacklist import BLACKLIST
from db import db
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
import os
from ma import ma
from models.user import UserModel
from resources.execution_result import ExecutionResult, NewExecutionResult
from resources.test_case import NewTestCase, TestCase, TestCaseList
from resources.user import UserRegister, UserLogin, TokenRefresh, UserLogout, Admin, User, UserList

app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")  # load default configs from default_config.py
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URI", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "zero"
jwt = JWTManager(app)

db.init_app(app)
api = Api(app)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.find_by_id(identity)
    if user.is_admin:
        return {"is_admin": True}
    return {"is_admin": False}


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return (
            jwt_payload["jti"] in BLACKLIST
    )  # Here we blacklist particular JWTs that have been created in the past.


api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(UserList, "/users")
api.add_resource(Admin, "/admin")

api.add_resource(NewExecutionResult, "/executions")
api.add_resource(ExecutionResult, "/execution_results/<int:test_asset_id>")
api.add_resource(NewTestCase, "/new_testcases")
api.add_resource(TestCase, "/testcase/<int:test_case_id>")
api.add_resource(TestCaseList, "/testcases")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    ma.init_app(app)
    app.run(port=5000, debug=True)
