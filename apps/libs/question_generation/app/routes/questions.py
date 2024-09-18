from fastapi import APIRouter, HTTPException, status

from app.schemas.questions import (QuestionAnswerListSchema,
                                   QuestionAnswerSchema, QuestionListSchema,
                                   QuestionSchema)
from app.schemas.resume import Resume
from app.schemas.resume_scored import ResumeScoreExtended
from app.schemas.vacancy import Vacancy
from app.schemas.vacancy_scored import VacancyScoreExtended
from lib.generation import gen_questionnaire, gen_tech_questions

generation_router = APIRouter()


@generation_router.get(
    path='/',
    summary='Hi!'
)
async def index():
    return "Generation"


@generation_router.post(
    "/tech_questions",
    summary="Generates technical interview questions based on job vacancy and resume",
    response_model=QuestionListSchema
)
async def tech_questions(resume: Resume, vacancy: Vacancy):
    try:
        questions = await gen_tech_questions(resume, vacancy)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse resume. {e}",
        )

    return questions


@generation_router.post(
    "/questionnaire",
    summary="Generates questionnaire based on job vacancy and resume",
    response_model=QuestionAnswerListSchema
)
async def questionnaire(resume: ResumeScoreExtended, vacancy: VacancyScoreExtended):
    questions = await gen_questionnaire(resume=resume.resume, vacancy=vacancy.vacancy)

    return questions
