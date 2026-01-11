from utils.text_utils import get_alphabet
from ciphers.caesar_cipher import caesar_decrypt


def caesar_bruteforce(text: str, lang: str = "EN") -> list[str]:
    up, _ = get_alphabet(lang)
    variants = []

    for key in range(len(up)):
        variants.append(f"key={key}: {caesar_decrypt(text, key, lang)}")

    return variants
