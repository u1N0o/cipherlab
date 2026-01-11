from utils.text_utils import get_alphabet

def _validate_sub_key(key: str, alphabet_up: str) -> str:
    key = key.strip()

    if len(key) != len(alphabet_up):
        raise ValueError("key and alphabet_up must be the same length")

    key_up = key.upper()

    if len(set(key_up)) != len(key_up):
        raise ValueError("key and alphabet_up must be unique")

    if any(ch not in alphabet_up for ch in key_up):
        raise ValueError("key contains invalid characters")

    return key_up

def substitution_encrypt(text: str, key: str, lang: str = "EN") -> str:
    up, lo = get_alphabet(lang)
    key_up = _validate_sub_key(key, up)
    key_lo = key_up.lower()

    res = []

    for ch in text:
        if ch in up:
            res.append(key_up[up.index(ch)])
        elif ch in lo:
            res.append(key_lo[lo.index(ch)])
        else:
            res.append(ch)

    return "".join(res)

def substitution_decrypt(text: str, key: str, lang: str = "EN") -> str:
    up, lo = get_alphabet(lang)
    key_up = _validate_sub_key(key, up)
    key_lo = key_up.lower()

    inv_up = {key_up[i]: up[i] for i in range(len(key_up))}
    inv_lo = {key_lo[i]: lo[i] for i in range(len(key_lo))}

    res = []
    for ch in text:
        if ch in inv_up:
            res.append(inv_up[ch])
        elif ch in inv_lo:
            res.append(inv_lo[ch])
        else:
            res.append(ch)

    return "".join(res)
