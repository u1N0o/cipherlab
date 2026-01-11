import base64

def base64_encode(text: str) -> str:
    data = text.encode("utf-8")
    encoded = base64.b64encode(data)
    return encoded.decode("ascii")

def base64_decode(b64_text: str) -> str:
    try:
        data = base64.b64decode(b64_text.encode("ascii"))
    except Exception:
        raise ValueError("Base64 decode error")
    return data.decode("utf-8", errors="replace")