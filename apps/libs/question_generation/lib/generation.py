from environs import Env
from openai import AsyncOpenAI as OpenAI

from apps.libs.question_generation.app.schemas.questions import QuestionAnswerListSchema, QuestionAnswerSchema, QuestionListSchema, QuestionSchema
from apps.libs.question_generation.app.schemas.resume import Resume
from apps.libs.question_generation.app.schemas.resume_scored import ResumeScore
from apps.libs.question_generation.app.schemas.vacancy import Vacancy
from apps.libs.question_generation.app.schemas.vacancy_scored import VacancyScore
from apps.libs.question_generation.app.utils import remove_numeration
from apps.libs.question_generation.lib.questionnaire_gen import check_empty, check_skills, compare_full_time
from apps.libs.question_generation.lib.templates import generation_prompt


env = Env()
env.read_env()

base_url = "https://igrouii3jfzhk4jslvakummdxq0zkudm.lambda-url.eu-central-1.on.aws/v1/"
client = OpenAI(base_url=base_url)


async def request_to_openai(messages):
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        temperature=0,
    )

    return response


async def gen_tech_questions(resume: Resume, vacancy: Vacancy):
    messages = []

    messages.append({
        "role": "user",
                "content": f"{generation_prompt['step_1'].format(vacancy)}"
    })
    response = await request_to_openai(messages)

    messages.append({
        "role": "assistant",
                "content": f"{response.choices[0].message.content}"
    })
    messages.append({
        "role": "user",
                "content": f"{generation_prompt['step_2'].format(resume)}"
    })

    response1 = await request_to_openai(messages)

    messages.append({
        "role": "assistant",
                "content": f"{response1.choices[0].message.content}"
    })
    messages.append({
        "role": "user",
                "content": f"{generation_prompt['step_3']}"
    })

    response2 = await request_to_openai(messages)

    messages.append({
        "role": "assistant",
                "content": f"{response2.choices[0].message.content}"
    })
    messages.append({
        "role": "user",
                "content": f"{generation_prompt['step_4']}"
    })

    response3 = await request_to_openai(messages)

    result_questions = f"{response2.choices[0].message.content}\n{response3.choices[0].message.content}"
    result_questions = remove_numeration(result_questions)

    questions_objects = [QuestionSchema(
        question=question) for question in result_questions.split('\n')]

    question_list_schema = QuestionListSchema(questions=questions_objects)

    return question_list_schema


async def gen_questionnaire(resume: ResumeScore, vacancy: VacancyScore):
    questions = []
    questions_empty = await check_empty(resume)
    questions += questions_empty

    questions_full_time = await compare_full_time(resume)
    if questions_full_time:
        questions += [questions_full_time]

    questions_skills = await check_skills(resume)
    if questions_skills:
        questions += [questions_skills]

    questions = QuestionAnswerListSchema(questions=questions)
    return questions
