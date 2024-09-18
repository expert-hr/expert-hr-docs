from pydantic import BaseModel, Field

from libs.hr_comparator.app.schemas.resume import ResumeScore


class TotalScore(BaseModel):
    resume: ResumeScore = ResumeScore()
    score: int | None = Field(0, description="Total comparison score.")
