from typing import List, Optional
from pydantic import BaseModel, Field


class ScoredItem(BaseModel):
    value: str | int | bool | None = Field(
        None, description="Value of resume or vacancy field.")
    score: float | None = Field(
        None, description="Resume or vacancy field score.")
    discrepancy: str = Field("", description="Discrepancy in field.")


class JobExperienceScore(BaseModel):
    company: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    dates: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    position: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    description: ScoredItem = ScoredItem(
        value=None, score=None, discrepancy="")
    job_hard_skills: ScoredItem = ScoredItem(
        value=None, score=None, discrepancy="")
    job_soft_skills: ScoredItem = ScoredItem(
        value=None, score=None, discrepancy="")


class EducationScore(BaseModel):
    level: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    dates: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    place: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    specialization: ScoredItem = ScoredItem(
        value=None, score=None, discrepancy="")


class AdditionalEducationScore(BaseModel):
    place: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    year: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    specialization: ScoredItem = ScoredItem(
        value=None, score=None, discrepancy="")


class LanguageScore(BaseModel):
    language: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    level: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")


class ResumeScore(BaseModel):
    name: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    gender: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    age: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    birth_date: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    number: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    mail_address: ScoredItem = ScoredItem(
        value=None, score=None, discrepancy="")
    additional_links: List[ScoredItem] = []
    city: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    additional_address: ScoredItem = ScoredItem(
        value=None, score=None, discrepancy="")
    citizenship: ScoredItem = ScoredItem(
        value=None, score=None, discrepancy="")
    relocation_readiness: ScoredItem = ScoredItem(
        value=None, score=None, discrepancy="")
    position: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    wanted_salary: ScoredItem = ScoredItem(
        value=None, score=None, discrepancy="")
    specializations: List[ScoredItem] = []
    full_time: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    offline: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")
    job_experience: List[JobExperienceScore] = []
    experience_years: ScoredItem = ScoredItem(
        value=None, score=None, discrepancy="")
    experience_months: ScoredItem = ScoredItem(
        value=None, score=None, discrepancy="")
    education: List[EducationScore] = []
    additional_educations: List[AdditionalEducationScore] = []
    languages: List[LanguageScore] = []
    skills: List[ScoredItem] = []
    about: ScoredItem = ScoredItem(value=None, score=None, discrepancy="")


class ResumeScoreExtended(BaseModel):
    resume: ResumeScore
    score: float = Field(1.0, description="Overall score.")
