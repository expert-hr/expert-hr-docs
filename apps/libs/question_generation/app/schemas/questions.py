from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class QuestionSchema(BaseModel):
    question: str = Field("", description="Question for tech interview")


class QuestionListSchema(BaseModel):
    questions: List[QuestionSchema]


class AnswerType(str, Enum):
    PERSONAL = 'single'
    GROUP = 'multiple'
    TEXT = 'text'


class QuestionAnswerSchema(QuestionSchema):
    type: AnswerType = Field(
        AnswerType.TEXT, description="Type of answer (single, multiple or open answer)")
    answers: Optional[List[str]] = Field(
        None, description="Answers for this question (if type is text, it will be None)")


class QuestionAnswerListSchema(BaseModel):
    questions: List[QuestionAnswerSchema]
