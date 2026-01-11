from math import gcd
from utils.text_utils import get_alphabet

def _modinv(a: int, m: int) -> int:
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("modular inverse does not exist")

def _check_keys(a: int, b: int, m: int ) -> None:
    if gcd(a, m) != 1:
        raise ValueError("key a should be mutually simple with m")

def affine_encrypt(text: str, a: int, b: int, lang: str = "EN") -> str:
    up, lo = get_alphabet(lang)
    m = len(up)
    _check_keys(a, b, m)
    b %= m

    res = []
    for ch in text:
        if ch in up:
            x = up.index(ch)
            y = (a * x + b) % m
            res.append(up[y])
        elif ch in lo:
            x = lo.index(ch)
            y = (a * x + b) % m
            res.append(lo[y])

        else:
            res.append(ch)
    return "".join(res)

def affine_decrypt(text: str, a: int, b: int, lang: str = "EN") -> str:
    up, lo = get_alphabet(lang)
    m = len(up)
    _check_keys(a, b, m)
    b %= m

    a_inv = _modinv(a, m)

    res = []
    for ch in text:
        if ch in up:
            y = up.index(ch)
            x = (a_inv * (y - b)) % m
            res.append(up[x])
        elif ch in lo:
            y = lo.index(ch)
            x = (a_inv * (y - b)) % m
            res.append(lo[x])
        else:
            res.append(ch)
    return "".join(res)



