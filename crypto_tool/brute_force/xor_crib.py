from __future__ import annotations

def _clean_hex(s: str) -> str:
    return ''.join(s.split())

def _xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def recover_partial_keys_from_crib(
        cipher_hex: str,
        know_plain: str,
        key_len: int,
        offset: int | None = None
) -> list[list[int | None]]:
    if key_len <= 0:
        raise ValueError('key_len must be > 0')

    c = bytes.fromhex(_clean_hex(cipher_hex))
    p = know_plain.encode('utf-8')

    if len(p) > len(c):
        return []

    offsets = [offset] if offset is not None else range(0, len(c) - len(p) + 1)
    candidates: list[list[int | None]] = []

    for pos in offsets:
        key: list[int | None] = [None] * key_len
        ok = True

        for i in range(len(p)):
            idx = (pos + i) % key_len
            kd = c[pos + i] ^ p[i]

            if key[idx] is None:
                key[idx] = kd
            elif key[idx] != kd:
                ok = False
                break
        if ok:
            candidates.append(key)
    return candidates

def partial_key_to_hex(partial_key: list[int | None]) -> str:
    return "".join("??" if b is None else f"{b:02x}" for b in partial_key)

def preview_with_partial_key(cipher_hex: str, partial_key: list[int | None], preview_len: int = 200) -> str:
    c = bytes.fromhex(_clean_hex(cipher_hex))
    L = len(partial_key)

    out = []
    for i, b in enumerate(c[:preview_len]):
        kb = partial_key[i % L]
        if kb is None:
            out.append("?")
        else:
            x = b ^ kb
            out.append(chr(x) if 32 <= x <= 126 else ".")
    return "".join(out)

def decrypt_with_key_hex(cipher_hex: str, key_hex: str) -> str:
    c = bytes.fromhex(_clean_hex(cipher_hex))
    k = bytes.fromhex(_clean_hex(key_hex))
    p = _xor_bytes(c, k)
    return p.decode("utf-8", errors="replace")