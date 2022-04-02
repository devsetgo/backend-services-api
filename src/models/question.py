# -*- coding: utf-8 -*-
from datetime import datetime
from enum import Enum
from io import IncrementalNewlineDecoder

from pydantic import BaseModel, Field, validator

# Shared properties


q: dict = {
    "location": "uk",
    "description": "This is a description of the question",
    "question_list": [
        {
            "question": "What is the best way to get a car?",
            "text_answer": True,
            "text_answer_required": True,
            "text_answer_visable": True,
            "select_answer": True,
            "select_answer_type": "true_false",
            "select_answer_visable": True,
            "attachement_answer": True,
            "attachement_answer_required": False,
            "attachement_answer_visable": True,
        }
    ],
    "version": "1.0",
    "date_created": datetime.utcnow(),
    "date_updated": datetime.utcnow(),
}


class SelectAnswerType(str, Enum):
    """
    definition of select answer types
    """
    yes_no = "yes_no"
    yes_no_maybe = "yes_no_maybe"


class QuestionLocation(str, Enum):
    """
    locations

    """
    usa = "usa"
    ireland = "ireland"
    uk = "uk"
    france = "france"
    mexico = "mexico"

class QuestionItems(BaseModel):
    """
    Question Items
    """
    question: str = Field(..., alias="question", max_length=500)
    text_answer: bool = Field(None, alias="textAnswer", example=True)
    text_answer_required: bool = Field(None, alias="textAnswerRequired", example=True)
    text_answer_visable: bool = Field(None, alias="textAnswerVisable", example=True)
    select_answer: bool = Field(None, alias="selectAnswer", example=True)
    select_answer_type: SelectAnswerType = Field(None, alias="selectAnswerType", example=SelectAnswerType.yes_no)
    select_answer_visable: bool = Field(None, alias="selectAnswerVisable", example=True)
    attachement_answer: bool = Field(None, alias="attachementAnswer", example=True)
    attachement_answer_required: bool = Field(None, alias="attachementAnswerRequired", example=False)
    attachement_answer_visable: bool = Field(None, alias="attachementAnswerVisable", example=True)

class QuestionBase(BaseModel):
    """
    Question Base
    """
    location: QuestionLocation = Field(..., alias="location", example=QuestionLocation.uk)
    description: str = Field(..., alias="description", max_length=500)
    question_list: list = Field(..., alias="questionList", example=[QuestionItems])
    version: str = Field(..., alias="version", example="1.0")
    date_created: datetime = Field(..., alias="dateCreated", default_factory=datetime.utcnow())
    date_updated: datetime = Field(..., alias="dateUpdated", default_factory=datetime.utcnow())


# class AuditLogBase(BaseModel):
#     app_id: str = Field(..., alias="appId", max_length=50)
#     reference_id: str = Field(None, alias="referenceId", max_length=50)
#     record_type: AuditTypes
#     record_str: str = Field(
#         None,
#         alias="recordStr",
#         min_length=5,
#         max_length=500,
#         example="Bob did something",
#     )
#     record_json: dict = Field(
#         None,
#         alias="recordJson",
#         example={"data": "is free form", "user": "Bob", "thing": "did something"},
#     )
#     date_created: datetime = Field(alias="dateCreated", default_factory=datetime.now())

#     @validator("record_str")
#     def record_str_blank(cls, v, values, **kwargs):
#         if "record_str" == None and values["record_dict"] == None:
#             raise ValueError("Either record_str or record_dict must have data.")
#         return v

#     @validator("record_json")
#     def record_json_blank(cls, v, values, **kwargs):
#         if "record_json" == None and values["record_str"] == None:
#             raise ValueError("Either recordStr or recordDict must have data.")
#         return v
