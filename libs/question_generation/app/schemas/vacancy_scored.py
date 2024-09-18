from typing import List
from pydantic import BaseModel, Field


class ScoredItem(BaseModel):
    value: str | int | bool | None = Field(
        None, description="Value of resume or vacancy field.")
    score: float | None = Field(
        None, description="Resume or vacancy field score.")
    discrepancy: str = Field("", description="Discrepancy in field.")


class VacancyEducationScore(BaseModel):
    education_required: ScoredItem = ScoredItem(
        value=None, score=None, discrepancy="")
    education_specialization: ScoredItem = ScoredItem(
        value=None, score=None, discrepancy="")


class VacancyScore(BaseModel):
    job_title: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    min_salary_rub: ScoredItem = ScoredItem(
        value=None, score=None, discrepancy="")
    max_salary_rub: ScoredItem = ScoredItem(
        value=None, score=None, discrepancy="")
    company: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    city: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    min_experience_years: ScoredItem = ScoredItem(
        value=None, score=None, discrepancy="")
    max_experience_years: ScoredItem = ScoredItem(
        value=None, score=None, discrepancy="")
    full_time: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    remote: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    education: List[VacancyEducationScore] = []
    duties: List[ScoredItem] = []
    requirements: List[ScoredItem] = []
    advantages: List[ScoredItem] = []
    working_conditions: List[ScoredItem] = []
    job_hard_skills: List[ScoredItem] = []
    job_soft_skills: List[ScoredItem] = []
    about: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")


class VacancyScoreExtended(BaseModel):
    vacancy: VacancyScore
    score: float = Field(1.0, description="Overall score.")
