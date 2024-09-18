from fastapi import APIRouter, HTTPException, status

from apps.libs.hr_comparator.app.schemas.resume import Resume
from apps.libs.hr_comparator.app.schemas.vacancy import Vacancy
from apps.libs.hr_comparator.app.schemas.total_score import TotalScore
from apps.libs.hr_comparator.lib.comparator import Comparator


router = APIRouter()


@router.post("/match")
def compare(vacancy: Vacancy, resume: Resume, config: str = "lib/comparator_config.yaml") -> TotalScore:
    comparator = Comparator(vacancy_path=vacancy, resume_path=resume, config_path=config)
    try:
        total_score = comparator.match()
    except Exception as exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Exception when calling Comparator.match(): {exception}.")

    return total_score
