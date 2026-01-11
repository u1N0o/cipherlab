import base64

def base32_encode(text: str) -> str:
    data = text.encode("utf-8")
    encoded = base64.b32encode(data)
    return encoded.decode("ascii")

def base32_decode(b32_text: str) -> str:
    try:
        data = base64.b32decode(b32_text.encode("ascii"), casefold=True)
    except Exception:
        raise ValueError("Base32 decode error")
    return data.decode("utf-8", errors="replace")


