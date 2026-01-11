def binary_encode(text:str) -> str:
    data = text.encode("utf-8")
    return "".join(format(b, "08b") for b in data)

def binary_decode(binary_text:str) -> str:
    try:
        bits = "".join(ch for ch in binary_text if ch in "01")

        if len(bits) % 8 != 0:
            raise ValueError("Binary string length must be multiple of 8")

        data = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    except Exception:
        raise ValueError("Binary decode error")

    return data.decode("utf-8", errors="replace")