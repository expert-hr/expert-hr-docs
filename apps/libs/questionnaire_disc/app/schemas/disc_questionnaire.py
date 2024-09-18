from typing import List
from pydantic import BaseModel, Field


class DISCQuestionListSchema(BaseModel):
    disc: List[List[str]]


class ScoreSchema(BaseModel):
    adaptive: List[float]
    natural: List[float]


class DISCScoresSchema(BaseModel):
    scores: ScoreSchema
