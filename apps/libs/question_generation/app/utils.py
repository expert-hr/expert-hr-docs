import re


def remove_numeration(text):
    # Поиск и удаление числовой нумерации с точкой и пробелом
    result = re.sub(r'^\d+\.\s', '', text, flags=re.MULTILINE)
    return result
