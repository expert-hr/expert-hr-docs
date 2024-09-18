import base64
from typing import Annotated, Union

from fastapi import APIRouter, File, HTTPException, status
from langchain.schema.output_parser import OutputParserException

from apps.libs.hr_parser.lib.chain import build_chain
from apps.libs.hr_parser.app.schemas import Resume, Vacancy
from apps.libs.hr_parser.app.utils import pdf_to_markdown, extract_images, detect_face

router = APIRouter()

from environs import Env

env = Env()
env.read_env()

@router.post("/vacancy")
async def parse(file: Annotated[bytes, File()]) -> Vacancy:
    vacancy_template = "Parse the following vacancy: \n{format_instructions} \n{text}"
    vacancy_text = pdf_to_markdown(file)
    chain = build_chain(Vacancy, vacancy_template)
    try:
        output = await chain.ainvoke({"text": vacancy_text})
    except (OutputParserException, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to parse."
        )

    return output


@router.post("/resume")
async def parse(file: Annotated[bytes, File()]) -> Resume:
    resume_template = "Parse the following resume: \n{format_instructions} \n{text}"
    resume_text = pdf_to_markdown(file)
    images = extract_images(file)
    photo = None

    for img in images:
        img = base64.b64encode(img.getvalue()).decode()
        img = f"data:image/png;{img}"
        if detect_face(img):
            photo = img
            break

    chain = build_chain(Resume, resume_template)
    try:
        output = await chain.ainvoke({"text": resume_text})
        output.photo = photo

    except (OutputParserException, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to parse."
        )
    return output
