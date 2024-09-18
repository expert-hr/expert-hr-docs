import json
from typing import List

from apps.libs.questionnaire_disc.app.schemas.disc_questionnaire import DISCQuestionListSchema, DISCScoresSchema, ScoreSchema


async def get_disc_questions() -> DISCQuestionListSchema:
    """Load questions for dict test from file and return

    Returns:
        DISCQuestionListSchema: questions
    """
    question_path = 'data\question_disc.json'

    with open(question_path, 'r', encoding='utf-8') as file:
        json_data = json.loads(file.read())

    return DISCQuestionListSchema(disc=json_data)


async def get_disc_score(disc_answers: DISCQuestionListSchema) -> DISCScoresSchema:
    """Get coordinates for plot from person's answers for the disk test

    Args:
        disc_answers (DISCQuestionListSchema): person's answers

    Returns:
        DISCScoresSchema: coordinates for adaptive and natural assessment
    """
    scores_path = 'data\disc_scores.json'

    with open(scores_path, 'r', encoding='utf-8') as file:
        scores = json.loads(file.read())

    adapt_scores = await get_adapt_score(disc_answers, scores)
    natural_score = await get_natural_score(disc_answers, scores)

    disc_scores = ScoreSchema(
        adaptive=adapt_scores,
        natural=natural_score
    )

    return DISCScoresSchema(scores=disc_scores)


async def get_adapt_score(disc_answers: DISCQuestionListSchema, scores: List) -> List:
    """Get coordinates for a adaptive assessment on the disk test

    Args:
        disc_answers (DISCQuestionListSchema): Person's answers
        scores (List): Values for answers

    Returns:
        List: 4 coordinates for adaptive score plot
    """
    one = 0
    two = 0
    three = 0
    four = 0

    max_one = 20
    max_two = 17
    max_three = 19
    max_four = 15

    for i, answers in enumerate(disc_answers.disc):
        score = scores[i][answers[0]]['max']
        if score == 1:
            one += 1
        elif score == 2:
            two += 1
        elif score == 3:
            three += 1
        elif score == 4:
            four += 1

    one_score = await get_coord(one, max_one)
    two_score = await get_coord(two, max_two)
    three_score = await get_coord(three, max_three)
    four_score = await get_coord(four, max_four)

    return [one_score, two_score, three_score, four_score]


async def get_natural_score(disc_answers: DISCQuestionListSchema, scores: List) -> List:
    """Get coordinates for a natural assessment on the disk test

    Args:
        disc_answers (DISCQuestionListSchema): Person's answers
        scores (List): Values for answers

    Returns:
        List: 4 coordinates for natural score plot
    """
    one = 0
    two = 0
    three = 0
    four = 0

    max_one = 21
    max_two = 19
    max_three = 19
    max_four = 16

    for i, answers in enumerate(disc_answers.disc):
        score = scores[i][answers[-1]]['min']
        if score == 1:
            one += 1
        elif score == 2:
            two += 1
        elif score == 3:
            three += 1
        elif score == 4:
            four += 1

    one_score = await get_coord(one, max_one, True)
    two_score = await get_coord(two, max_two, True)
    three_score = await get_coord(three, max_three, True)
    four_score = await get_coord(four, max_four, True)

    return [one_score, two_score, three_score, four_score]


async def get_coord(score: int, max_value_score: int, inverse: bool = False) -> float:
    """Normalizes the coordinate from 0 to 1 and inverts it if necessary

    Args:
        score (int): Human parameter score
        max_value_score (int): highest possible score
        inverse (bool, optional): True if need inverts score (1 - score). Defaults to False.

    Returns:
        float: final score/coord for diagram 
    """
    if score != 0:
        score = round(score / max_value_score, 2)
    else:
        score = 0.0

    if inverse:
        score = 1 - score

    return score
