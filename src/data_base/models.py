# -*- coding: utf-8 -*-
# from tortoise import fields, models
# from tortoise.contrib.pydantic import pydantic_model_creator


# class Users(models.Model):
#     """
#     The User model
#     """

#     id = fields.UUIDField(pk=True)
#     #: This is a username
#     user_name = fields.CharField(max_length=20, unique=True)
#     email = fields.CharField(max_length=50, null=True)
#     password = fields.CharField(max_length=50, null=True)
#     category = fields.CharField(max_length=30, default="misc")
#     password_hash = fields.CharField(max_length=128, null=True)
#     created_at = fields.DatetimeField(auto_now_add=True)
#     modified_at = fields.DatetimeField(auto_now=True)
#     # Column("notes", String(length=2000)),
#     # Column("date_created", DateTime()),
#     # Column("date_updated", DateTime()),
#     # Column("last_login", DateTime()),
#     # Column("is_active", Boolean(), default=True),
#     # Column("is_superuser", Boolean(), default=True),
#     # Column("is_approved", Boolean(), default=False),
#     def full_name(self) -> str:
#         """
#         Returns the best name
#         """
#         if self.name or self.family_name:
#             return f"{self.name or ''} {self.family_name or ''}".strip()
#         return self.username

#     class PydanticMeta:
#         # computed = ["full_name"]
#         exclude = ["password"]


# User_Pydantic = pydantic_model_creator(Users, name="User")
# UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)
