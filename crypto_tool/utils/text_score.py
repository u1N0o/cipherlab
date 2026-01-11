from __future__ import annotations


def score_text(s: str) -> float:
    """
    Simple readability scoring:
    - printable ratio
    - spaces
    - basic punctuation
    """
    if not s:
        return -1e9

    printable_ok = 0
    for ch in s:
        if ch.isprintable() and ch not in "\x0b\x0c":
            printable_ok += 1
    ratio = printable_ok / len(s)

    bonus = 0.0
    bonus += s.count(" ") * 0.6
    bonus += sum(s.count(c) for c in ".,!?;:") * 0.2

    return ratio * 10.0 + bonus
