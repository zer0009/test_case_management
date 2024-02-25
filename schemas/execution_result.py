# # from models.execution_result import ExecutionResultModel
# #
# # from marshmallow import Schema, fields
# # from ma import ma
# # from models import *
# #
# #
# # class ExecutionResultSchema(ma.SQLAlchemyAutoSchema):
# #     class Meta:
# #         model = ExecutionResultModel
# #         # load_only = ("user",)
# #         dump_only = ("id",)
# #         load_instance = True
# #         include_relationships = True
# #         include_fk = True
#
#
# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
# from models import *
# from models.execution_result import ExecutionResultModel
# from ma import ma
#
#
# class ExecutionResultSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = ExecutionResultModel
#         dump_only = ("id",)
#         load_instance = True
#         include_relationships = True
#         include_fk = True
