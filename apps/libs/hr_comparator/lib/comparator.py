import re
from deep_translator import GoogleTranslator
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from json import JSONDecodeError
import json

from apps.libs.hr_comparator.app.schemas.resume import Resume, ResumeScore, ResumeScoredItem
from apps.libs.hr_comparator.app.schemas.vacancy import Vacancy
from apps.libs.hr_comparator.app.schemas.total_score import TotalScore
from apps.libs.hr_comparator.lib.utils import load_data_from_json, load_data_from_yaml


core_language_list = ["(python)$", "(java)$", "c\\+\\+", "(c)$", "(javascript)$", "(c#)$", "(go)$", "(typescript)$", "(html)$", "(css)$", "(php)$"]


def clear_non_alphabet_symbols(text):
    cleaned_text = re.sub(r"[^a-zA-Zа-яА-Я]", " ", text).lower().split()
    return cleaned_text


def translate_text(text):
    """Translates text from one language to English.
    Args:
        text (str): Text to be translated.
    """
    try:
        translated_text = GoogleTranslator(source="ru", target="en").translate(text)
        return translated_text
    except:
        return text


class Comparator:
    """Compare vacancy and resume fields.
    See criteria evaluation for more information.

    Args:
        vacancy_path (str | Vacancy): Path to the vacancy JSON file or schema object.
        resume_path (str | Resume)): Path to the resume JSON file or schema object.
        config_path (str): Path to the weight configuration file.
    """

    def __init__(self, vacancy_path: str | Vacancy, resume_path: str | Resume, config_path: str) -> None:
        if isinstance(vacancy_path, str):
            vacancy_path = load_data_from_json(vacancy_path)
            vacancy_path = Vacancy(**vacancy_path)
        if isinstance(resume_path, str):
            resume_path = load_data_from_json(resume_path)
            resume_path = Resume(**resume_path)
        self.vacancy = vacancy_path
        self.resume = resume_path
        self.resume_score = ResumeScore()
        self.weight_config = load_data_from_yaml(config_path)

    def _fill_nulls(self, type="str") -> str | int | list:
        """Fill nulls in the fields."""
        if type == "str":
            return ""
        if type == "int":
            return 0
        if type == "list":
            return []

    def _compare_city(self) -> None:
        """Compare "city" field from vacancy and resume."""
        if not isinstance(self.resume.city, str):
            self.resume.city = self._fill_nulls(type="str")
        if self.vacancy.city:
            if self.vacancy.city == self.resume.city:
                self.resume_score.city = ResumeScoredItem(value=self.resume.city, score=1)
            else:
                self.resume_score.city = ResumeScoredItem(value=self.resume.city, score=0)
        else:
            self.resume_score.city = ResumeScoredItem(value=self.resume.city, score=None)

    def _compare_position(self) -> None:
        """Compare "position" field from vacancy and resume."""
        if not isinstance(self.resume.position, str):
            self.resume.position = self._fill_nulls(type="str")
        if self.vacancy.job_title:
            # Preprocess and translate job title
            job_title = clear_non_alphabet_symbols(self.vacancy.job_title)
            job_title = [translate_text(word) for word in job_title]
            # Preprocess and translate desired position
            resume_position = clear_non_alphabet_symbols(self.resume.position)
            resume_position = [translate_text(word) for word in resume_position]
            if set(job_title).intersection(resume_position):
                self.resume_score.position = ResumeScoredItem(value=self.resume.position, score=1)
            else:
                self.resume_score.position = ResumeScoredItem(value=self.resume.position, score=0)
        else:
            self.resume_score.position = ResumeScoredItem(value=self.resume.position, score=None)

    def _compare_wanted_salary(self) -> None:
        """Compare "wanted_salary" field from vacancy and resume."""
        if not isinstance(self.resume.wanted_salary, int):
            self.resume.wanted_salary = self._fill_nulls(type="int")
        if all([not self.vacancy.min_salary_rub, not self.vacancy.max_salary_rub]):
            self.resume_score.wanted_salary = ResumeScoredItem(value=self.resume.wanted_salary, score=None)
        if not self.resume.wanted_salary:
            self.resume_score.wanted_salary = ResumeScoredItem(value=self.resume.wanted_salary, score=None)
        if self.vacancy.max_salary_rub:
            if self.vacancy.max_salary_rub >= self.resume.wanted_salary:
                self.resume_score.wanted_salary = ResumeScoredItem(value=self.resume.wanted_salary, score=1)
            else:
                self.resume_score.wanted_salary = ResumeScoredItem(value=self.resume.wanted_salary, score=0)

    def _compare_full_time(self) -> None:
        """Compare "full_time" field from vacancy and resume."""
        if not isinstance(self.resume.full_time, bool):
            self.resume_score.full_time = ResumeScoredItem(value=self.resume.full_time, score=None)
        else:
            if self.vacancy.full_time:
                if self.vacancy.full_time == self.resume.full_time:
                    self.resume_score.full_time = ResumeScoredItem(value=self.resume.full_time, score=1)
                else:
                    self.resume_score.full_time = ResumeScoredItem(value=self.resume.full_time, score=0)
            else:
                self.resume_score.full_time = ResumeScoredItem(value=self.resume.full_time, score=None)

    def _compare_offline(self) -> None:
        """Compare "offline" field from vacancy and resume."""
        if not isinstance(self.resume.offline, bool):
            self.resume_score.offline = ResumeScoredItem(value=self.resume.offline, score=None)
        else:
            if self.vacancy.remote:
                if self.vacancy.remote and not self.resume.offline:
                    self.resume_score.offline = ResumeScoredItem(value=self.resume.offline, score=1)
                else:
                    self.resume_score.offline = ResumeScoredItem(value=self.resume.offline, score=0)
            else:
                self.resume_score.offline = ResumeScoredItem(value=self.resume.offline, score=None)

    def _compare_job_experience(self) -> None:
        """Compare "job_experience" field from vacancy and resume."""
        if not isinstance(self.resume.job_experience, list):
            self.resume.job_experience = self._fill_nulls(type="list")
        if not isinstance(self.vacancy.job_hard_skills, list):
            self.vacancy.job_hard_skills = self._fill_nulls(type="list")
        if self.vacancy.job_title:
            # Preprocess and translate job title
            job_title = clear_non_alphabet_symbols(self.vacancy.job_title)
            job_title = [translate_text(word) for word in job_title]
            for job in self.resume.job_experience:
                # Preprocess and translate job experience position
                resume_position = clear_non_alphabet_symbols(job.position)
                resume_position = [translate_text(word) for word in resume_position]
                if set(job_title).intersection(resume_position):
                    self.resume_score.job_experience.append(ResumeScoredItem(value=dict(job), score=1))
                else:
                    self.resume_score.job_experience.append(ResumeScoredItem(value=dict(job), score=0))
        else:
            for job in self.resume.job_experience:
                self.resume_score.job_experience.append(ResumeScoredItem(value=dict(job), score=None))

    def _compare_experience_years(self) -> None:
        """Compare "experience_years" field from vacancy and resume."""
        if not isinstance(self.resume.experience_years, int):
            self.resume.experience_years = self._fill_nulls(type="int")
        if not isinstance(self.resume.experience_months, int):
            self.resume.experience_months = self._fill_nulls(type="int")
        if all([not self.vacancy.min_experience_years, not self.vacancy.max_experience_years]):
            self.resume_score.experience_years = ResumeScoredItem(value=self.resume.experience_years, score=None)
            self.resume_score.experience_months = ResumeScoredItem(value=self.resume.experience_months, score=None)
        if self.vacancy.max_experience_years:
            if self.vacancy.max_experience_years >= self.resume.experience_years:
                self.resume_score.experience_years = ResumeScoredItem(value=self.resume.experience_years, score=1)
                self.resume_score.experience_months = ResumeScoredItem(value=self.resume.experience_months, score=1)
            else:
                self.resume_score.experience_years = ResumeScoredItem(value=self.resume.experience_years, score=0)
                self.resume_score.experience_months = ResumeScoredItem(value=self.resume.experience_months, score=0)
        if self.vacancy.min_experience_years:
            if self.vacancy.min_experience_years <= self.resume.experience_years:
                self.resume_score.experience_years = ResumeScoredItem(value=self.resume.experience_years, score=1)
                self.resume_score.experience_months = ResumeScoredItem(value=self.resume.experience_months, score=1)
            else:
                self.resume_score.experience_years = ResumeScoredItem(value=self.resume.experience_years, score=0)
                self.resume_score.experience_months = ResumeScoredItem(value=self.resume.experience_months, score=0)

    def _compare_education(self) -> None:
        """Compare "education" field from vacancy and resume."""
        if not isinstance(self.resume.education, list):
            self.resume.education = self._fill_nulls(type="list")
        if not isinstance(self.resume.additional_educations, list):
            self.resume.additional_educations = self._fill_nulls(type="list")
        if isinstance(self.vacancy.education, list):
            for required_education in self.vacancy.education:
                required_specialization = clear_non_alphabet_symbols(required_education.education_specialization)
                for education in self.resume.education:
                    resume_education = clear_non_alphabet_symbols(education.specialization)
                    if set(required_specialization).intersection(resume_education):
                        self.resume_score.education.append(ResumeScoredItem(value=dict(education), score=1))
                    else:
                        self.resume_score.education.append(ResumeScoredItem(value=dict(education), score=0))
                for add_education in self.resume.additional_educations:
                    add_education_spec = clear_non_alphabet_symbols(add_education.specialization)
                    if set(required_specialization).intersection(add_education_spec):
                        self.resume_score.additional_educations.append(ResumeScoredItem(value=dict(add_education), score=1))
                    else:
                        self.resume_score.additional_educations.append(ResumeScoredItem(value=dict(add_education), score=0))
        else:
            for education in self.resume.education:
                self.resume_score.education.append(ResumeScoredItem(value=dict(education), score=None))
            for add_education in self.resume.additional_educations:
                self.resume_score.additional_educations.append(ResumeScoredItem(value=dict(add_education), score=None))

    def _compare_education_with_llm(self) -> str:
        template = """You have a resume and a job vacancy. Compare the education levels mentioned in the resume with the job description.
        Evaluate how well the candidate's education fits the vacancy requirements, responding using the “score” key. “score” can be 0 or 1, where 0 - means definitely
        mismatch, 1 - means fits the vacancy's requirements. The specialization may not coincide completely; having a higher education is sufficient.

        Here is the resume:
        {resume}
        End of resume.

        Next is the vacancy:
        {vacancy}
        End of vacancy.

        Response exclusively in json format duplicating the original structure and the content of the resume.
        The answer should be exclusively in the format without any other comments:
        {{"education":[.., score:...], "additional_educations":[.., "score":...]}}
        """
        vacancy = {
            "education topics": [education.education_specialization for education in self.vacancy.education],
            "requirements": self.vacancy.requirements,
        }
        resume = {
            "education": self.resume.education,
            "additional_educations": self.resume.additional_educations,
        }
        prompt = PromptTemplate(input_variables=["vacancy", "resume"], template=template)
        llm_chain = LLMChain(
            llm=ChatOpenAI(model="gpt-3.5-turbo-16k"),
            prompt=prompt,
            verbose=False,
        )

        reqs_res = llm_chain.predict(vacancy=vacancy, resume=resume)
        return reqs_res

    def _compare_skills(self) -> None:
        """Compare "skills" field from vacancy and resume."""
        if not isinstance(self.resume.skills, list):
            self.resume.skills = self._fill_nulls(type="list")
        if not isinstance(self.vacancy.job_hard_skills, list):
            self.vacancy.job_hard_skills = self._fill_nulls(type="list")
        job_hard_skills = [skill.lower() for skill in self.vacancy.job_hard_skills]
        job_hard_skills = [translate_text(skill) for skill in job_hard_skills]
        resume_skills = [skill.lower() for skill in self.resume.skills]
        resume_skills = [translate_text(skill) for skill in resume_skills]
        for skill in self.resume.skills:
            if translate_text(skill.lower()) in job_hard_skills:
                self.resume_score.skills.append(ResumeScoredItem(value=skill, score=1))
            else:
                self.resume_score.skills.append(ResumeScoredItem(value=skill, score=None))
        for skill in self.vacancy.job_hard_skills:
            if translate_text(skill.lower()) not in resume_skills:
                self.resume_score.skills.append(ResumeScoredItem(value=skill, score=0))

    def _compare_core_skill(self) -> int:
        """Compare core skills from vacancy and resume."""
        job_hard_skills = [skill.lower() for skill in self.vacancy.job_hard_skills]
        job_hard_skills = [translate_text(skill) for skill in job_hard_skills]
        resume_skills = [skill.lower() for skill in self.resume.skills]
        resume_skills = [translate_text(skill) for skill in resume_skills]
        for job_skill in job_hard_skills:
            for core_lang in core_language_list:
                if re.match(core_lang, job_skill):
                    if job_skill in resume_skills:
                        return 1
                    else:
                        return 0
        return 1

    def _compare_requirements_with_llm(self) -> str:
        template = """You have a resume and a job vacancy. You need to analyze the "job_experience" section in the resume;
        "job_title" and "requirements" in the vacancy. Compare how well the сandidate's previous work experience 
        fits the vacancy requirements, responding using the “score” key. “score” can be 0 or 1, where 0 means definitely
        not suitable, 1 means suitable or contains similar position.

        Here is the resume:
        {resume}
        End of resume.

        Next is the vacancy:
        {vacancy}
        End of vacancy.

        Response exclusively in json format duplicating the structure and the content of the Resume.
        The answer should be exclusively in the format without any other comments:
        {{"job_experience":[.., "score":...]}}
        """

        vacancy = {"job_title": self.vacancy.job_title, "requirements": self.vacancy.requirements}
        resume = {"job_experience": self.resume.job_experience}
        prompt = PromptTemplate(input_variables=["vacancy", "resume"], template=template)

        llm_chain = LLMChain(
            llm=ChatOpenAI(model="gpt-3.5-turbo-16k"),
            prompt=prompt,
            verbose=False,
        )

        reqs_res = llm_chain.predict(vacancy=vacancy, resume=resume)
        return reqs_res

    def _calculate_total_score(self) -> int:
        """Calculate total score for the resume."""
        v11 = self.resume_score.wanted_salary.score if isinstance(self.resume_score.wanted_salary.score, int) else 1
        v12 = self.resume_score.full_time.score if isinstance(self.resume_score.full_time.score, int) else 1
        v13 = self.resume_score.offline.score if isinstance(self.resume_score.offline.score, int) else 1
        v21 = self.resume_score.experience_years.score if isinstance(self.resume_score.experience_years.score, int) else 1
        v22_counter = 0
        if isinstance(self.vacancy.education, list):
            for education in self.resume_score.education:
                if isinstance(education.score, int):
                    v22_counter += education.score
            v22 = 1 if v22_counter >= 1 else 0
        else:
            v22 = 1
        if isinstance(self.vacancy.job_hard_skills, list):
            v31 = self._compare_core_skill()
            v32_counter, v32_sum = 0, 0
            for skill in self.resume_score.skills:
                if isinstance(skill.score, int):
                    v32_sum += skill.score
                    v32_counter += 1
            try:
                v32 = v32_sum / v32_counter
            except ZeroDivisionError:
                v32 = 0
        else:
            v31 = 1
            v32 = 1
        if isinstance(self.vacancy.job_hard_skills, list):
            v41_counter = 0
            for job in self.resume_score.job_experience:
                if isinstance(job.score, int):
                    v41_counter += job.score
            v41 = 1 if v41_counter >= 1 else 0
        else:
            v41 = 1
        g1 = self.weight_config["criteria"]["w11"] * v11 + self.weight_config["criteria"]["w12"] * v12 + self.weight_config["criteria"]["w13"] * v13
        g2 = self.weight_config["criteria"]["w21"] * v21 + self.weight_config["criteria"]["w22"] * v22
        g3 = self.weight_config["criteria"]["w31"] * v31 + self.weight_config["criteria"]["w32"] * v32
        g4 = self.weight_config["criteria"]["w41"] * v41

        return int(
            sum(
                [
                    self.weight_config["groups"]["w1"] * g1,
                    self.weight_config["groups"]["w2"] * g2,
                    self.weight_config["groups"]["w3"] * g3,
                    self.weight_config["groups"]["w4"] * g4,
                ]
            )
            * 100
        )

    def compare_fields(self) -> ResumeScore:
        """Compare fields from vacancy and resume."""
        self._compare_city()
        self._compare_position()
        self._compare_wanted_salary()
        self._compare_full_time()
        self._compare_offline()
        self._compare_experience_years()
        try:
            response = self._compare_requirements_with_llm()
            requirements_score = json.loads(response)
            print(requirements_score)
            for field in requirements_score["job_experience"]:
                self.resume_score.job_experience.append(ResumeScoredItem(value=field, score=field["score"]))
        except (JSONDecodeError, TypeError, KeyError):
            self._compare_job_experience()
        try:
            response = self._compare_education_with_llm()
            requirements_score = json.loads(response)
            for field in requirements_score["additional_educations"]:
                self.resume_score.additional_educations.append(ResumeScoredItem(value=field, score=field["score"]))
            for field in requirements_score["education"]:
                self.resume_score.education.append(ResumeScoredItem(value=field, score=field["score"]))
        except (JSONDecodeError, TypeError, KeyError):
            self._compare_education()
        self._compare_skills()
        return self.resume_score

    def match(self) -> TotalScore:
        total_score = TotalScore()
        self.resume_score = self.compare_fields()
        total_score.resume = self.resume_score
        total_score.score = self._calculate_total_score()
        return total_score
