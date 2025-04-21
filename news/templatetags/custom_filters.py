from django import template

register = template.Library()

CENSOR_WORDS = ['Редиска', 'Жесть']

@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError(f'Фильтр censor можно применять только к строкам! Получен: {type(value)}')

    divided_s = value.split()
    censored_words = []

    for word in divided_s:
        clean_word = word.strip('.,!?;:-_()[]{}"\'')

        if clean_word.capitalize() in CENSOR_WORDS:
            clean_word = word[0] + '*' * (len(clean_word) - 1) + word[len(clean_word):]
            censored_words.append(clean_word)
        else:
            censored_words.append(word)
    return ' '.join(censored_words)