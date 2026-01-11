from __future__ import annotations
def _clean_hex(s: str) -> str:
    return "".join(s.split())

def _xor_bytes(data: bytes, key: bytes) -> bytes:
    if not key:
        raise ValueError("key is required")
    res = bytearray()
    for i, b in enumerate(data):
        res.append(b ^ key[i % len(key)])
    return bytes(res)

def xor_encrypt(plain_text: str, key: str, key_type: str = "text") -> str:
    data = plain_text.encode("utf-8")
    if key_type == "text":
        key_bytes = key.encode("utf-8")
    elif key_type == "hex":
        key_bytes = bytes.fromhex(_clean_hex(key))
    else:
        raise ValueError("key_type must be text or hex")
    encrypted = _xor_bytes(data, key_bytes)
    return encrypted.hex()

def xor_decrypt(cipher_hex: str, key: str, key_type: str = "text") -> str:
    data = bytes.fromhex(_clean_hex(cipher_hex))
    if key_type == "text":
        key_bytes = key.encode("utf-8")
    elif key_type == "hex":
        key_bytes = bytes.fromhex(_clean_hex(key))
    else:
        raise ValueError("key_type must be text or hex")

    decrypted = _xor_bytes(data, key_bytes)
    return decrypted.decode("utf-8", errors="replace")
