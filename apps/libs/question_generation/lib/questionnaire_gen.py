from typing import List

from apps.libs.question_generation.app.schemas.questions import AnswerType, QuestionAnswerSchema
from apps.libs.question_generation.app.schemas.resume_scored import ResumeScore
from apps.libs.question_generation.lib.questions_and_fields import (compare_full_time_field, empty_fields,
                                      question_fields)


async def check_empty(resume_score: ResumeScore) -> List[QuestionAnswerSchema]:
    question = []

    for field in empty_fields:
        field_value = getattr(resume_score, field)

        if field_value.value is None:
            question.append(QuestionAnswerSchema(
                question=question_fields[field],
                type=AnswerType.TEXT
            ))

    return question


async def compare_full_time(resume_score: ResumeScore) -> QuestionAnswerSchema | None:
    field_name = compare_full_time_field['resume_field']
    if getattr(resume_score, field_name).score < 1:
        if getattr(resume_score, field_name).value is True:
            return QuestionAnswerSchema(
                question=question_fields['full_time_no'],
                type=AnswerType.TEXT
            )
        else:
            return QuestionAnswerSchema(
                question=question_fields['full_time_yes'],
                type=AnswerType.TEXT
            )

    return None


async def check_skills(resume_score: ResumeScore) -> QuestionAnswerSchema | None:
    skills_question = []

    for skill in resume_score.skills:
        if skill.score == 0:
            skills_question.append(skill.value)

    if skills_question:
        return QuestionAnswerSchema(
            question=question_fields['skills'],
            type=AnswerType.GROUP,
            answers=skills_question
        )

    return None
