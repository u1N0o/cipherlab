def hex_encode(text: str) -> str:
    data = text.encode("utf-8")
    return data.hex()

def hex_decode(hex_text: str) -> str:
    try:
        data = bytes.fromhex("".join(hex_text.split()))
    except Exception:
        raise ValueError("Hex decode error")

    return data.decode("utf-8", errors="replace")