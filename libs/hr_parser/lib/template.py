resume_template = """
Отформатируй текст под следующий json шаблон:
           "name": ,
           "gender": ,
           "age"(int): ,
           "birth_date": ,
           "number": ,
           "mail_address": ,
           "additional_links": [],
           "city": ,
           "additional_address": ,
           "citizenship": ,
           "relocation_readiness": ,
           "position": ,
           "wanted_salary"(int): ,
           "specializations": [],
           "full_time"(bool): ,
           "offline"(bool): ,
           "job_experience": [
           "company": ,
           "dates": ,
           "position": ,
           "description": ,
           "job_hard_skills": ,
           "job_soft_skills": ,
            ],
           "experience_years": ,
           "experience_months": ,
           "education": [
           "level": ,
           "dates" ,
           "place" ,
           "specialization": ,
           ],
           "additional_educations": [
           "place": ,
           "year": ,
           "specialization": ,
           ],
           "languages": [
           "language": ,
           "level": ,
           ]
           "skills": [],
           "about":

        Поля "job_hard_skills" и "job_soft_skills" из "job_experience" должны содержать навыки указанные в описании опыта на выбранном рабочем месте.
        В случае, если информация о "description", "position" и навыках отсутствует, возвращать пустую строку.
        Текст для обработки: 
"""

vacancy_template = """Отформатируй текст под следующий json шаблон:
           "job_title"(str): ,
           "min_salary_rub"(int): ,
           "max_salary_rub"(int): ,
           "company"(str): ,
           "city"(str): ,
           "min_experience_years"(int): ,
           "max_experience_years"(int): ,
           "full_time"(bool): ,
           "remote"(bool): ,
           "education": [\{
                "education_required"(bool):,
                "education_specialization"(str):
           \},],
           "duties": [
           ],
           "requirements": [
           ],
           "advantages": [
           ],
           "working_conditions": [
           ],
           "job_soft_skills": [
           ],
           "job_hard_skills": [
           ],
           "about"(str): " "
           Пояснение: education должен иметь тип list, education_specialization означает направленность(профиль) образования, например: техническое, медицинское, финансовое и так далее; "duties" означает обязанности или основные задачи; "advantages" означает умения, которые необязательны, но будут преимуществом для кандидата; "working_conditions" означает предлагаемые условия работы.
           Текст для обработки: 
"""
