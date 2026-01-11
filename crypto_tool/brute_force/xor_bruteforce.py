from __future__ import annotations
import itertools
import string
from typing import Iterable


def _clean_hex(s: str) -> str:
    return "".join(s.split())

def _xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def _score_text(s: str) -> float:
    if not s:
        return -1e9

    printable_ok = 0
    for ch in s:
        if ch.isprintable() and ch not in "\x0b\x0c":
            printable_ok += 1
    ratio = printable_ok / len(s)

    bonus = 0.0
    bonus += s.count(" ") * 0.6
    bonus += sum(s.count(c) for c in ".,!?-:;") * 0.2

    letters = sum(ch.isalpha() for ch in s)
    bonus += (letters / len(s)) * 5.0

    return ratio * 10.0 + bonus

def _keyspace(alphabet: str) -> Iterable[int]:
    alphabet = alphabet.lower()
    if alphabet == "bytes":
        return range(256)

    if alphabet == "printable":
        chars = (string.ascii_letters + string.digits + string.punctuation + " ")

        return  [ord(c) for c in dict.fromkeys(chars)]
    raise ValueError("alphabet not supported")

def estimate_variants_count(key_len: int, alphabet: str) -> int:
    space = len(list(_keyspace(alphabet)))

    return space ** key_len

def xor_bruteforce(
        cipher_hex: str,
        key_len: int,
        alphabet: str = "bytes",
        top_n: int = 20,
        preview_len: int = 200,
        max_variants: int = 2_000_000
) -> list[dict]:
    if key_len <= 0:
        raise ValueError("key_len must be > 0")

    data = bytes.fromhex(_clean_hex(cipher_hex))
    ks = list(_keyspace(alphabet))
    variants_count = (len(ks) ** key_len)

    if variants_count > max_variants:
        raise ValueError("Too many variants")

    best: list[dict] = []

    for tup in itertools.product(ks, repeat=key_len):
        key = bytes(tup)
        plain_bytes = _xor_bytes(data, key)
        plain = plain_bytes.decode("utf-8")

        sc = _score_text(plain)

        item = {
            "key_hex": key.hex(),
            "key_text": key.decode("utf-8", errors="replace"),
            "score": sc,
            "preview": plain[:preview_len]
        }

        if len(best) < top_n:
            best.append(item)
            best.sort(key=lambda x: x["score"], reverse=True)
        else:
            if sc > best[-1]["score"]:
                best[-1] = item
                best.sort(key=lambda x: x["score"], reverse=True)

    return best




















