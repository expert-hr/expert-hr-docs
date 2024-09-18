from typing import List, Optional

from pydantic import BaseModel


class Education(BaseModel):
    education_required: bool | None
    education_specialization: Optional[str] | None


class Vacancy(BaseModel):
    job_title: str | None
    min_salary_rub: int | None
    max_salary_rub: int | None
    company: str | None
    city: str | None
    min_experience_years: int | None
    max_experience_years: int | None
    full_time: bool | None
    remote: bool | None
    education: List[Education] | None = []
    duties: List[str] | None = []
    requirements: List[str] | None = []
    advantages: List[str] | None = []
    working_conditions: List[str] | None = []
    job_hard_skills: List | None = []
    job_soft_skills: List | None = []
    about: str | None
