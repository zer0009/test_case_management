from marshmallow import pre_dump

from ma import ma
from models.user import UserModel
from models import *


# very important don't delete!!! => this must be load first because they have an relationship with fax


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        # load_only = ( "faxes", "note",)
        dump_only = ("id",)
        load_instance = True

        include_relationships = True
        include_fk = True
