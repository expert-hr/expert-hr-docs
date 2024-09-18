from typing import List, Optional

from pydantic import BaseModel


class JobExperience(BaseModel):
    company: str
    dates: str | int
    position: str
    description: Optional[str]
    job_hard_skills: Optional[str]
    job_soft_skills: Optional[str]


class Education(BaseModel):
    level: str
    dates: str | int
    place: str
    specialization: Optional[str]


class AdditionalEducation(BaseModel):
    place: str
    year: str | int
    specialization: Optional[str]


class Language(BaseModel):
    language: str
    level: str


class Resume(BaseModel):
    name: str | None
    gender: str | None
    age: int | None
    birth_date: str | None
    number: str | None
    mail_address: str | None
    additional_links: List[str] | None = []
    city: str | None
    additional_address: str | None
    citizenship: str | None
    relocation_readiness: str | None
    position: str | None
    wanted_salary: int | None
    specializations: List[str] = []
    full_time: bool | None
    offline: bool | None
    job_experience: List[JobExperience] = []
    experience_years: int | None
    experience_months: int | None
    education: List[Education] | None = []
    additional_educations: List[AdditionalEducation] | None = []
    languages: List[Language] | None = []
    skills: List[str] | None = []
    about: str | None
