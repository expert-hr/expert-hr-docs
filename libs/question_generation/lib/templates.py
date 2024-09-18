generation_prompt = {
    "step_1": """Вы - интервьюер, который зарабатывает 200$ в час за свою работу, проводящий собеседование на эту роль: {}. Какие ключевые hard skills должны быть у кандидата, а также какими теоретическими знаниями и в каких областях должен владеть кандидат.""",
    "step_2": """На эту вакансию проходит техническое собеседование кандидат, вот его CV: {}. Выдели его основные навыки и hard skills и оцени насколько кандидат подходит для этой вакансии.""",
    "step_3": """Теперь сгенерируй 10 вопросов для технического собеседования для проверки знаний кандидата на данную позицию. 
                        Постарайся задавать вопросы в 1 предложение. Это должны быть конкретные вопросы на проверку теоретических и практических знаний. Не пиши ничего кроме вопросов.""",
    "step_4": """Сгенерируй еще 10 вопросов для технического собеседования для проверки знаний кандидата на данную позицию. Постарайся задавать вопросы в 1 предложение. 
                        Это должны быть усложненные технические, теоретические и практические вопросы больше углубись в проверку навыков кандидата, задай вопросы, ответы на которые должен знать кандидат при условии, что у него есть опыт работы. 
                        Вопросы не должны повторяться с прошлыми. Не пиши ничего кроме вопросов."""
}
