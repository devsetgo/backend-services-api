# -*- coding: utf-8 -*-
from datetime import datetime
from doctest import Example
from enum import Enum
from io import IncrementalNewlineDecoder

from pydantic import BaseModel, Field, validator

# Shared properties


q: dict = {
    "type": "task",
    "question": "What is the best way to get a car?",
    "description": "This is a description of the question",
    "text_options": "is_optional",
    "select_options": "is_optional",
    "attachement_options": "is_optiona",
    "version": "1.0",
    "is_active": True,
    "is_approved": True,
    "date_created": datetime.utcnow(),
    "date_updated": datetime.utcnow(),
    "created_by": "admin",
    "updated_by": "admin",
}


class AnswerOptions(str, Enum):
    """
    definition of answer options
    """

    is_optional = "is_optional"
    is_required = "is_required"
    is_hidden = "is_hidden"


class QuestionBase(BaseModel):
    """
    definition of question
    """

    question: str = Field(
        ..., min_length=5, max_length=500, example="What is the best way to get a car?"
    )
    description: str = Field(
        ..., min_length=5, max_length=500, example="Please describe the question"
    )
    text_options: AnswerOptions = Field(
        ..., min_length=5, max_length=50, example="is_optional"
    )
    select_options: AnswerOptions = Field(
        ..., min_length=5, max_length=50, example="is_required"
    )
    attachement_options: AnswerOptions = Field(
        ..., min_length=5, max_length=50, example="is_hidden"
    )
    version: int
    is_active: bool = Field(..., example=True)
    is_approved: bool = Field(..., example=True)
    date_created: datetime = Field(..., example=datetime.utcnow())
    date_updated: datetime = Field(..., example=datetime.utcnow())
    created_by: str = Field(..., max_length=50)
    updated_by: str = Field(..., max_length=50)
