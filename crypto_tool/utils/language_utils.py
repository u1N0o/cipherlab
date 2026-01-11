from utils.vigenere_analysis import guess_language

def choose_lang(text: str, user_lang: str | None) -> str:
    """
    user_lang:
      - 'EN' / 'RU' -> берём как есть
      - None / 'AUTO' -> угадываем
    """
    if user_lang is None:
        return guess_language(text)[0]

    user_lang = user_lang.strip().upper()
    if user_lang in ("EN", "RU"):
        return user_lang

    if user_lang in ("AUTO", ""):
        return guess_language(text)[0]

    return "EN"
