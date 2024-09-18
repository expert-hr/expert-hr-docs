from typing import List
from pydantic import BaseModel, Field


class VacancyEducation(BaseModel):
    education_required: bool | None = None
    education_specialization: str | None = None


class Vacancy(BaseModel):
    job_title: str | None = None
    min_salary_rub: int | None = None
    max_salary_rub: int | None = None
    company: str | None = None
    city: str | None = None
    min_experience_years: int | None = None
    max_experience_years: int | None = None
    full_time: bool | None = None
    remote: bool | None = None
    education: List[VacancyEducation] | None = []
    duties: List[str] | None = []
    requirements: List[str] | None = []
    advantages: List[str] | None = []
    working_conditions: List[str] | None = []
    job_hard_skills: List[str] | None = []
    job_soft_skills: List[str] | None = []
    about: str | None = None
