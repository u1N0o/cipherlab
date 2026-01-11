from utils.text_utils import get_alphabet


def caesar_cipher(text: str, n: int, lang: str = "EN") -> str:
    up, lo = get_alphabet(lang)
    res = []
    n = n % len(up)

    for ch in text:
        if ch in up:
            i = up.index(ch)
            res.append(up[(i + n) % len(up)])
        elif ch in lo:
            i = lo.index(ch)
            res.append(lo[(i + n) % len(lo)])
        else:
            res.append(ch)

    return "".join(res)

def rot13(text: str) -> str:
    return caesar_cipher(text, 13, "EN")

def caesar_encrypt(text: str, n: int, lang: str = "EN") -> str:
    return caesar_cipher(text, n, lang)


def caesar_decrypt(text: str, n: int, lang: str = "EN") -> str:
    return caesar_cipher(text, -n, lang)
