from __future__ import annotations
from typing import Optional

from ciphers.caesar_cipher import caesar_decrypt
from utils.text_utils import get_alphabet
from utils.text_score import score_text


def detect_caesar_shift(cipher_text: str, lang: str = "EN") -> tuple[Optional[int], float, str]:
    """
    Returns:
      best_shift, best_score, best_plain
    """
    up, _ = get_alphabet(lang)
    m = len(up)

    best_shift = None
    best_score = -1e9
    best_plain = ""

    for shift in range(1, m + 1):
        plain = caesar_decrypt(cipher_text, shift, lang)
        sc = score_text(plain)
        if sc > best_score:
            best_score = sc
            best_shift = shift
            best_plain = plain

    return best_shift, best_score, best_plain
