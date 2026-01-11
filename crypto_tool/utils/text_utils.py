import string

EN_UP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
EN_LO = "abcdefghijklmnopqrstuvwxyz"

RU_UP = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
RU_LO = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def get_alphabet(lang: str = "EN"):
    """
    Возвращает кортеж (upper_alphabet, lower_alphabet)
    lang: 'EN' или 'RU'
    """
    lang = lang.upper()
    if lang == "EN":
        return EN_UP, EN_LO
    elif lang == "RU":
        return RU_UP, RU_LO
    else:
        raise ValueError("Язык должен быть 'EN' или 'RU'")


def shift_char(ch: str, shift: int, alphabet_up: str, alphabet_lo: str) -> str:
    """
    Сдвиг символа по алфавиту (для Цезаря/ROT).
    Неизвестные символы возвращаются как есть.
    """
    if ch in alphabet_up:
        idx = alphabet_up.index(ch)
        return alphabet_up[(idx + shift) % len(alphabet_up)]
    if ch in alphabet_lo:
        idx = alphabet_lo.index(ch)
        return alphabet_lo[(idx + shift) % len(alphabet_lo)]
    return ch


def is_printable_text(s: str) -> bool:
    """
    Проверка, что строка примерно читаемая.
    Используется в brute-force.
    """
    printable = set(string.printable) | set(RU_LO) | set(RU_UP)
    if not s:
        return False
    good = sum(1 for c in s if c in printable)
    return good / len(s) > 0.85
