from fastapi import APIRouter, HTTPException, status

from app.schemas.disc_questionnaire import DISCQuestionListSchema, DISCScoresSchema
from lib.disc_questions import get_disc_questions, get_disc_score


disc_router = APIRouter()


@disc_router.get(
    path='/',
    summary='Hi!'
)
async def index():
    return "DISC"


@disc_router.get(
    "/questions",
    summary="Returns a list of phrase lists for the disc test",
    response_model=DISCQuestionListSchema
)
async def questionnaire():
    questions = await get_disc_questions()

    return questions


@disc_router.post(
    "/score",
    summary="Returns the disk score for a person",
    response_model=DISCScoresSchema
)
async def questionnaire(disc_answers: DISCQuestionListSchema):
    scores = await get_disc_score(disc_answers)

    return scores
