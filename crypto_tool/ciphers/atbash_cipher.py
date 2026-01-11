from utils.text_utils import get_alphabet

def atbash_transform(text: str, lang: str = "EN") -> str:
    up, lo = get_alphabet(lang)

    res = []
    for ch in text:
        if ch in up:
            i = up.index(ch)
            res.append(up[-1 - i])
        elif ch in lo:
            i = lo.index(ch)
            res.append(lo[-1 - i])
        else:
            res.append(ch)

    return "".join(res)


# Для удобства (чтобы в GUI было понятно)
def atbash_encrypt(text: str, lang: str = "EN") -> str:
    return atbash_transform(text, lang)

def atbash_decrypt(text: str, lang: str = "EN") -> str:
    return atbash_transform(text, lang)
