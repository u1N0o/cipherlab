from __future__ import annotations
from utils.text_utils import get_alphabet


def _normalize_key(key: str, lang: str) -> str:
    up, lo = get_alphabet(lang)
    allowed = set(up) | set(lo)
    key_letters = [ch.upper() for ch in key if ch in allowed]
    if not key_letters:
        raise ValueError("Key must contain at least one alphabet letter for selected language.")
    return "".join(key_letters)


def vigenere_encrypt(text: str, key: str, lang: str = "EN") -> str:
    up, lo = get_alphabet(lang)
    key = _normalize_key(key, lang)

    res = []
    j = 0

    for ch in text:
        if ch in up:
            shift = up.index(key[j % len(key)])
            res.append(up[(up.index(ch) + shift) % len(up)])
            j += 1
        elif ch in lo:
            shift = up.index(key[j % len(key)])  # key in upper alphabet
            res.append(lo[(lo.index(ch) + shift) % len(lo)])
            j += 1
        else:
            res.append(ch)

    return "".join(res)


def vigenere_decrypt(text: str, key: str, lang: str = "EN") -> str:
    up, lo = get_alphabet(lang)
    key = _normalize_key(key, lang)

    res = []
    j = 0

    for ch in text:
        if ch in up:
            shift = up.index(key[j % len(key)])
            res.append(up[(up.index(ch) - shift) % len(up)])
            j += 1
        elif ch in lo:
            shift = up.index(key[j % len(key)])
            res.append(lo[(lo.index(ch) - shift) % len(lo)])
            j += 1
        else:
            res.append(ch)

    return "".join(res)
