from __future__ import annotations
from collections import Counter
from typing import Dict, List, Tuple

from utils.text_utils import get_alphabet


def normalize_text(text: str, lang: str) -> str:
    """Оставляет только буквы выбранного алфавита, в UPPER."""
    up, lo = get_alphabet(lang)
    allowed = set(up) | set(lo)
    filtered = [ch.upper() for ch in text if ch in allowed]
    return "".join(filtered)


def index_of_coincidence(text: str, lang: str) -> float:
    """
    IC = sum(f_i*(f_i-1)) / (N*(N-1))
    где f_i — частоты букв, N — длина текста.
    """
    t = normalize_text(text, lang)
    n = len(t)
    if n < 2:
        return 0.0

    freq = Counter(t)
    num = sum(f * (f - 1) for f in freq.values())
    den = n * (n - 1)
    return num / den


def average_ic_for_keylen(text: str, key_len: int, lang: str) -> float:
    """
    Разбивает текст на key_len подпоследовательностей и усредняет IC.
    """
    t = normalize_text(text, lang)
    if key_len <= 0:
        raise ValueError("key_len must be > 0")
    if len(t) < 2 * key_len:
        # слишком мало данных — оценка будет шумной
        return 0.0

    parts = [t[i::key_len] for i in range(key_len)]
    ics = [index_of_coincidence(p, lang) for p in parts if len(p) >= 2]
    return sum(ics) / len(ics) if ics else 0.0


def guess_language(text: str) -> Tuple[str, Dict[str, float]]:
    """
    Пробует EN/RU и выбирает где больше букв алфавита.
    Возвращает (best_lang, scores_dict).
    """
    # считаем долю символов, которые попали в алфавит
    scores: Dict[str, float] = {}
    for lang in ("EN", "RU"):
        up, lo = get_alphabet(lang)
        allowed = set(up) | set(lo)
        total_letters = sum(1 for ch in text if ch.isalpha())
        if total_letters == 0:
            scores[lang] = 0.0
        else:
            in_alphabet = sum(1 for ch in text if ch in allowed)
            scores[lang] = in_alphabet / total_letters

    best = max(scores, key=scores.get)
    return best, scores


def suggest_vigenere_key_lengths(
    text: str,
    lang: str | None = None,
    max_len: int = 20,
    top_n: int = 5
) -> List[Tuple[int, float]]:
    """
    Возвращает топ длин ключа по среднему IC: [(key_len, avg_ic), ...]
    """
    if lang is None:
        lang, _ = guess_language(text)

    results: List[Tuple[int, float]] = []
    for k in range(1, max_len + 1):
        avg_ic = average_ic_for_keylen(text, k, lang)
        results.append((k, avg_ic))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_n]
