from typing import List, Optional
from pydantic import BaseModel, Field


class JobExperience(BaseModel):
    company: str | None = Field(None, description="Name of the company")
    dates: str | None = Field(None, description="Dates of working in form mm.yy")
    position: str | None = Field(None, description="The position name")
    description: str | None = Field(
        None, description="The description of the tasks and projects of the job"
    )
    job_hard_skills: List[str] | None = Field(
        None, description="The list of the hard skills mentioned on the description"
    )
    job_soft_skills: List[str] | None = Field(
        None, description="The list of the soft skills mentioned on the description"
    )


class Education(BaseModel):
    level: str | None = Field(None, description="Level of education")
    dates: str | None = Field(None, description="Dates of styding in form mm.yy")
    place: str | None = Field(None, description="Name of the university")
    specialization: str | None = Field(None, description="Domain of the education")


class AdditionalEducation(BaseModel):
    place: str | None = Field(None, description="The name of the course organization")
    year: int | None = Field(None, description="The year of the course's end")
    specialization: str | None = Field(None, description="The domain of the course")


class Language(BaseModel):
    language: str | None = Field(None, description="The name of the language")
    level: str | None = Field(None, description="The level of the language")


class Resume(BaseModel):
    photo: str | None = None

    name: str | None = Field(
        None, description="Name of the person (if exist, else empty)"
    )
    gender: str | None = Field(None, description="Gender of the person: Male | Female")
    age: int | None = Field(None, description="The age of the person.")
    birth_date: str | None = Field(
        None, description="The birth date of the person in format dd.mm.yyyy"
    )
    number: str | None = Field(None, description="Phone number of the person.")
    mail_address: str | None = Field(None, description="Email of the person.")
    additional_links: List[str] | None = Field(
        None, description="Links mentioned in the contantact info."
    )
    city: str | None = Field(None, description="Mentioned city of the person.")
    additional_address: str | None = Field(
        None, description="Info about location, it can be subway station"
    )
    citizenship: str | None = Field(None, description="Country name")
    relocation_readiness: List[str] | None = Field(
        None, description="Info about relocation, it can contain countries"
    )
    position: str | None = Field(None, description="Naming of the resume job position")
    wanted_salary: int | None = Field(
        None,
        description="Mentioned salary. None if did't mention. Lower value, if it is a range",
    )
    specializations: List[str] | None = Field(
        None,
        description="The list with job domains, which are listed after the specific word",
    )
    full_time: bool | None = Field(None, description="The readiness to full time job")
    offline: bool | None = Field(
        None, description="The readiness to work only from office"
    )
    job_experience: List[JobExperience] | None = Field(
        None,
        description="The list contains the dictionary with specific keys for every mentioned job",
    )
    experience_years: int | None = Field(
        None, description="Total number of job experience years"
    )
    experience_months: int | None = Field(
        None, description="Total number of job experience months"
    )
    education: List[Education] | None = Field(
        None,
        description="The list contains the dictionaries with specific keys for every mentioned university",
    )
    additional_educations: List[AdditionalEducation] | None = Field(
        None,
        description="The list contains the dictionaries with specific keys for every mentioned course",
    )
    languages: List[Language] | None = Field(
        None,
        description="The list contains the dictionaries with specific keys for every mentioned language",
    )
    skills: List[str] | None = Field(
        None, description="The list of mentioned skills in the corresponding section"
    )
    about: str | None = Field(
        None, description="Information about the person, mentioned after skills"
    )
