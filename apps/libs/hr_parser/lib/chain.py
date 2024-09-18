from typing import Annotated, Union
from apps.libs.hr_parser.app.schemas import Resume, Vacancy

from langchain.chains import LLMChain
from langchain.output_parsers import OutputFixingParser
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chat_models.openai import ChatOpenAI


def build_chain(
    pydantic_object: Union[Vacancy, Resume],
    template: str,
    model: str = "gpt-4-turbo-preview",
    temperature: float = 0.1,
    max_retries: int = 25,
) -> LLMChain:
    parser = PydanticOutputParser(pydantic_object=pydantic_object)
    format_instructions = parser.get_format_instructions()
    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template(template),
        ],
        input_variables=["text"],
        partial_variables={"format_instructions": format_instructions}
    )

    model = ChatOpenAI(model=model, temperature=temperature)

    return prompt | model | OutputFixingParser.from_llm(llm=model, parser=parser, max_retries=max_retries)
