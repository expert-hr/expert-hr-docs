from typing import List
from pydantic import BaseModel, Field


class ResumeJobExperience(BaseModel):
    company: str | None = None
    dates: str | None = None
    position: str | None = None
    description: str | None = None
    job_hard_skills: str | list | None = None
    job_soft_skills: str | list | None = None


class ResumeEducation(BaseModel):
    level: str | None = None
    dates: str | int | None = None
    place: str | None = None
    specialization: str | None = None


class ResumeAdditionalEducation(BaseModel):
    place: str | None = None
    year: str | int | None = None
    specialization: str | None = None


class ResumeLanguage(BaseModel):
    language: str | None = None
    level: str | None = None


class Resume(BaseModel):
    name: str | None = None
    gender: str | None = None
    age: int | None = None
    birth_date: str | None = None
    number: str | None = None
    mail_address: str | None = None
    additional_links: List[str] | None = []
    city: str | None = None
    additional_address: str | None = None
    citizenship: str | None = None
    relocation_readiness: str | None = None
    position: str | None = None
    wanted_salary: int | None = None
    specializations: List[str] = []
    full_time: bool | None = None
    offline: bool | None = None
    job_experience: List[ResumeJobExperience] | None = []
    experience_years: int | None = None
    experience_months: int | None = None
    education: List[ResumeEducation] | None = []
    additional_educations: List[ResumeAdditionalEducation] | None = []
    languages: List[ResumeLanguage] | None = []
    skills: List[str] | None = []
    about: str | None = None


class ResumeScoredItem(BaseModel):
    value: str | int | bool | list | dict |None = Field(None, description="Value of the field.")
    score: int | float | None = Field(None, description="Score of the field.")


class ResumeScore(BaseModel):
    city: ResumeScoredItem | None = ResumeScoredItem(value=None, score=None)
    position: ResumeScoredItem | None = ResumeScoredItem(value=None, score=None)
    wanted_salary: ResumeScoredItem | None = ResumeScoredItem(value=None, score=None)
    full_time: ResumeScoredItem | None = ResumeScoredItem(value=None, score=None)
    offline: ResumeScoredItem | None = ResumeScoredItem(value=None, score=None)
    job_experience: List[ResumeScoredItem] | None = []
    experience_years: ResumeScoredItem | None = ResumeScoredItem(value=None, score=None)
    experience_months: ResumeScoredItem | None = ResumeScoredItem(value=None, score=None)
    education: List[ResumeScoredItem] | None = []
    additional_educations: List[ResumeScoredItem] | None = []
    skills: List[ResumeScoredItem] | None = []
