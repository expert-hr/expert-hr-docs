import enum

from pydantic import BaseModel, Field
from typing import List


class Education(BaseModel):
    education_required: bool | None = Field(
        None,
        description="If education is required - True, if it is optional \
                                             or does not mentioned - False",
    )
    education_specialization: str | None = Field(
        None,
        description="Specialization of education, this field should be filled in only \
                                                  if education_required == true and education_specialization is specified, else None",
    )


class Vacancy(BaseModel):
    job_title: str | None = Field(None, description="Job title (if exist, else None)")
    min_salary_rub: int | None = Field(
        None, description="Minimum value of the proposed salary (if exist, else None)"
    )
    max_salary_rub: int | None = Field(
        None, description="Maximum value of the proposed salary (if exist, else None)"
    )
    company: str | None = Field(
        None, description="Name of the company (if exist, else None)"
    )
    city: str | None = Field(
        None, description="City, mentioned in the text (if exist, else None)"
    )
    min_experience_years: int | None = Field(
        None, description="Minimum required years of experience (if exist, else None)"
    )
    max_experience_years: int | None = Field(
        None, description="Maximum required years of experience (if exist, else None)"
    )
    full_time: bool | None = Field(
        None,
        description="If only full time job is available - True, if other options are availbale - False, else None",
    )
    remote: bool | None = Field(
        None,
        description="If remote job is available - True, if only offline job is available - False, else None",
    )
    education: List[Education] | None = Field(
        None,
        description="List contains the dictionaries with specific keys for every mentioned education",
    )
    duties: List[str] | None = Field(
        None, description="List contains duties or main tasks"
    )
    requirements: List[str] | None = Field(
        None, description="List contains requirements for the job"
    )
    advantages: List[str] | None = Field(
        None,
        description="List contains candidate skills that are optional, but will be an advantage for the candidate",
    )
    working_conditions: List[str] | None = Field(
        None, description="List contains working conditions"
    )
    job_hard_skills: List | None = Field(
        None, description="The list of technical skills required for a job"
    )
    job_soft_skills: List | None = Field(
        None,
        description="The list of required soft skills mentioned in the vacancy, soft skills means personal qualities required for a job, like: ответственность, внимательность",
    )
    about: str | None = Field(
        None, description="Main information about the company and the vacancy"
    )
