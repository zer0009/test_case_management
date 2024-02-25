import traceback
from flask import request
from flask_restful import Resource
from blacklist import BLACKLIST
from models.user import UserModel
from hmac import compare_digest
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)

from schemas.user import UserSchema

user_schema = UserSchema()
user_schema_list = UserSchema(many=True)


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())

        if UserModel.find_by_username(user.username):
            return {"message": "A user with that username already exists"}, 400

        try:
            user.save_to_db()
            return {"message": "User created successfully."}, 201
        except:
            traceback.print_exc()
            user.delete_from_db()
            return {"message": "failed to created User."}, 500


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        """This endpoint is used for get user information."""
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user_schema.dump(user), 200

    @classmethod
    @jwt_required()
    def delete(cls, user_id: int):
        """This endpoint is used for deactivated the user not delete the user because if the user deleted
        everything the user made will delete also."""
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user_id_login = get_jwt_identity()
        claims = get_jwt()
        if (user_id == user_id_login) or claims["is_admin"]:
            user.save_to_db()
        # user.delete_from_db()
        return {"message": "owner user privilege required "}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        """This endpoint is used for login the user, the user must enter username and password correctly
        and be activated and he must be confirmed his email."""
        user_json = request.get_json()
        user_data = user_schema.load(
            user_json, partial=("name",)
        )

        user = UserModel.find_by_username(user_data.username)

        if user and compare_digest(user.password, user_data.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       "access_token": access_token,
                       "refresh_token": refresh_token,
                       "user_id": user.id,
                   }, 200
        return {"message": "Invalid Credentials!"}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        """This endpoint is used for logout the user."""
        jti = get_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class Admin(Resource):
    @classmethod
    def post(cls):
        """This endpoint is used for register the admin it must not be public."""
        admin_json = request.get_json()
        admin_json["is_admin"] = True
        admin = user_schema.load(admin_json)

        if UserModel.find_by_username(admin.username):
            return {"message": "A admin with that username already exists"}, 400

        if UserModel.find_by_email(admin.name):
            return {"message": "The Name already exists"}, 400

        admin.save_to_db()

        return {"message": "admin created successfully."}, 201


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        """
        Get a new access token without requiring username and password—only the 'refresh token'
        provided in the /login endpoint.
        Note that refreshed access tokens have a `fresh=False`, which means that the user may have not
        given us their username and password for potentially a long time (if the token has been
        refreshed many times over).
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


class UserList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        """This endpoint is used for getting all users in database only  the admin can get this lest."""
        claims = get_jwt()
        if not claims["is_admin"]:
            return {"message": "Admin privilege required."}, 401
        return {"Users": [user_schema_list.dump(UserModel.find_all())]}
