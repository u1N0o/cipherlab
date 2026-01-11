# main.py — CipherLab CLI (English UI)

from __future__ import annotations

# --- ciphers ---
from ciphers import (
    caesar_encrypt, caesar_decrypt, rot13,
    atbash_transform,
    affine_encrypt, affine_decrypt,
    substitution_encrypt, substitution_decrypt,
    xor_encrypt, xor_decrypt,
    vigenere_encrypt, vigenere_decrypt
)

# --- codecs (renamed from encodings to avoid stdlib conflict) ---
from codecs_lab import (
    base64_encode, base64_decode,
    base32_encode, base32_decode,
    hex_encode, hex_decode,
    binary_encode, binary_decode,
)

# --- brute force / analysis ---
from brute_force import (
    caesar_bruteforce,
    xor_bruteforce,
    recover_partial_keys_from_crib,
    partial_key_to_hex,
    preview_with_partial_key,
)

# --- vigenere analysis ---
from utils.vigenere_analysis import (
    guess_language,
    index_of_coincidence,
    suggest_vigenere_key_lengths,
)

from utils.language_utils import choose_lang

from utils.caesar_detect import detect_caesar_shift

BANNER = r"""
 ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗ ██╗      █████╗ ██████╗ 
██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗██║     ██╔══██╗██╔══██╗
██║     ██║██████╔╝███████║█████╗  ██████╔╝██║     ███████║██████╔╝
██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗██║     ██╔══██║██╔══██╗
╚██████╗██║██║     ██║  ██║███████╗██║  ██║███████╗██║  ██║██████╔╝
 ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ 

   CipherLab CLI — Encrypt • Decrypt • Analyze
"""

# ==========================================================
# CLI helpers
# ==========================================================

def pause() -> None:
    input("\n[Enter] Continue...")


def ask_lang(default: str = "AUTO") -> str:
    lang = input(f"Language (AUTO/EN/RU) [{default}]: ").strip().upper()
    if not lang:
        lang = default

    if lang in ("AUTO", "EN", "RU"):
        return lang

    print("Invalid language. Using AUTO.")
    return "AUTO"



def ask_int(prompt: str, default: int | None = None) -> int:
    while True:
        s = input(prompt).strip()
        if s == "" and default is not None:
            return default
        try:
            return int(s)
        except ValueError:
            print("Error: please enter an integer.")


def safe_run(func):
    try:
        func()
    except Exception as e:
        print(f"\n[Error] {e}")
        pause()


# ==========================================================
# Analyzer: detect format and SUGGEST actions
# ==========================================================

def _clean_hex(s: str) -> str:
    return "".join(s.split())


def _is_hex_like(s: str) -> bool:
    t = _clean_hex(s)
    if len(t) < 2 or len(t) % 2 != 0:
        return False
    allowed = set("0123456789abcdefABCDEF")
    return all(ch in allowed for ch in t)


def _is_binary_like(s: str) -> bool:
    # allow spaces/newlines, but only 0/1 as meaningful chars
    bits = [ch for ch in s if ch in "01"]
    if len(bits) < 8:
        return False
    # if there are any other characters besides whitespace and 0/1 -> not binary
    if not all(ch in "01 \n\t\r" for ch in s):
        return False
    return len(bits) % 8 == 0


def _looks_like_base64(s: str) -> bool:
    t = "".join(s.split())
    if len(t) < 8:
        return False
    allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=")
    if not all(ch in allowed for ch in t):
        return False
    return len(t) % 4 == 0


def _looks_like_base32(s: str) -> bool:
    t = "".join(s.split()).upper()
    if len(t) < 8:
        return False

    allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567=")
    if not all(ch in allowed for ch in t):
        return False

    # avoid misclassifying simple uppercase text (like "KHOOR ZRUOG")
    has_markers = any(ch in "234567=" for ch in t)
    length_like = (len(t) % 8 == 0)
    return has_markers or length_like

def analyzer_actions(data: str) -> list[str]:
    """
    Order is important:
    - detect HEX/BINARY first so they won't be treated as text
    - then base64/base32
    - text as fallback (with Caesar/Atbash/Vigenere analysis)
    """
    if _is_hex_like(data):
        return [
            "Detected: HEX",
            "1) Hex decode -> text",
            "2) XOR brute-force (cipher_hex)",
            "3) XOR crib attack (known plaintext)",
        ]

    if _is_binary_like(data):
        return [
            "Detected: BINARY",
            "1) Binary decode -> text",
        ]

    if _looks_like_base64(data):
        return [
            "Detected: BASE64 (likely)",
            "1) Base64 decode -> text",
            "2) Try Base32 decode",
        ]

    if _looks_like_base32(data):
        return [
            "Detected: BASE32 (possible)",
            "1) Base32 decode -> text",
            "2) Try Base64 decode",
        ]

    # TEXT (or ciphers on text)
    # Even if not strictly _is_text_like, show text actions as fallback.
    return [
        "Detected: TEXT (or Caesar/Atbash/Vigenere)",
        "1) Caesar auto-detect (best ROT)",
        "2) Atbash transform",
        "3) Vigenere IC analysis (guess language & key length)",
    ]


def run_analyzer():
    print("\n=== Analyzer ===")
    data = input("Paste input string: ").strip()

    if not data:
        print("Empty input.")
        pause()
        return

    actions = analyzer_actions(data)

    print("\nAnalyzer result:")
    for line in actions:
        print(line)
    print("0) Back")

    choice = input("\nSelect: ").strip()

    # HEX branch
    if actions[0].startswith("Detected: HEX"):
        if choice == "1":
            print("\nDecoded:")
            print(hex_decode(data))
            pause()

        elif choice == "2":
            key_len = ask_int("Key length (1-3 recommended) [1]: ", default=1)
            top_n = ask_int("Show TOP N results [10]: ", default=10)

            best = xor_bruteforce(
                cipher_hex=data,
                key_len=key_len,
                alphabet="printable",   # no extra prompt, faster than bytes
                top_n=top_n
            )

            print("\nTOP results:")
            for item in best:
                print(f"\nscore={item['score']:.2f}")
                print("key_hex :", item["key_hex"])
                print("key_text:", item["key_text"])
                print("preview :", item["preview"])

            pause()

        elif choice == "3":
            key_len = ask_int("Key length: ")
            known_plain = input("Known plaintext (crib): ")
            off_s = input("Offset (byte position, Enter if unknown): ").strip()
            offset = int(off_s) if off_s else None

            candidates = recover_partial_keys_from_crib(
                cipher_hex=data,
                known_plain=known_plain,
                key_len=key_len,
                offset=offset
            )

            if not candidates:
                print("\nNo candidates found.")
                pause()
                return

            print(f"\nCandidates found: {len(candidates)}")
            for pk in candidates[:10]:
                print("\npartial_key_hex:", partial_key_to_hex(pk))
                print("preview:", preview_with_partial_key(data, pk))

            pause()

        return

    # BINARY branch
    if actions[0].startswith("Detected: BINARY"):
        if choice == "1":
            print("\nDecoded:")
            print(binary_decode(data))
            pause()
        return

    # BASE64 branch
    if actions[0].startswith("Detected: BASE64"):
        if choice == "1":
            print("\nDecoded:")
            print(base64_decode(data))
            pause()
        elif choice == "2":
            print("\nDecoded:")
            print(base32_decode(data))
            pause()
        return

    # BASE32 branch
    if actions[0].startswith("Detected: BASE32"):
        if choice == "1":
            print("\nDecoded:")
            print(base32_decode(data))
            pause()
        elif choice == "2":
            print("\nDecoded:")
            print(base64_decode(data))
            pause()
        return

    # TEXT branch
    if actions[0].startswith("Detected: TEXT"):
        if choice == "1":
            lang_guess, _ = guess_language(data)
            best_shift, best_score, best_plain = detect_caesar_shift(data, lang_guess)

            if best_shift is None:
                print("\nCaesar not detected (text too short or not suitable).")
            else:
                print(f"\nBest Caesar guess: ROT {best_shift}")
                print(best_plain)

            pause()


        elif choice == "2":
            lang = choose_lang(data, "AUTO")    
            print("\nAtbash result:")
            print(atbash_transform(data, lang))
            pause()

        elif choice == "3":
            guessed_lang, scores = guess_language(data)
            ic = index_of_coincidence(data, guessed_lang)
            top = suggest_vigenere_key_lengths(
                data,
                lang=guessed_lang,
                max_len=20,
                top_n=10
            )

            print("\nVigenere IC analysis:")
            print(f"Language guess: {guessed_lang} (scores: EN={scores['EN']:.2f}, RU={scores['RU']:.2f})")
            print(f"IC (whole text): {ic:.4f}")
            print("\nTop key lengths by avg IC:")
            for k, val in top:
                print(f"  key_len={k:<2}  avg_IC={val:.4f}")

            print("\nTip: high avg_IC for some key_len often indicates Vigenere key length.")
            pause()

        return


# ==========================================================
# Menus
# ==========================================================

def show_main_menu():
    print("\n=== Main Menu ===")
    print("1) Ciphers")
    print("2) Codecs")
    print("3) Analyzer")
    print("0) Exit")


def show_ciphers_menu():
    print("\n--- Ciphers ---")
    print("1) Caesar Encrypt")
    print("2) Caesar Decrypt")
    print("3) Caesar Brute-force")
    print("4) ROT13 (EN)")
    print("5) Atbash (RU/EN)")
    print("6) Affine Encrypt")
    print("7) Affine Decrypt")
    print("8) Substitution Encrypt")
    print("9) Substitution Decrypt")
    print("10) XOR Encrypt (text -> hex)")
    print("11) XOR Decrypt (hex -> text)")
    print("12) Vigenere Encrypt")
    print("13) Vigenere Decrypt")
    print("0) Back")


def show_codecs_menu():
    print("\n--- Codecs ---")
    print("1) Base64 encode")
    print("2) Base64 decode")
    print("3) Base32 encode")
    print("4) Base32 decode")
    print("5) Hex encode")
    print("6) Hex decode")
    print("7) Binary encode")
    print("8) Binary decode")
    print("0) Back")


def run_ciphers():
    while True:
        show_ciphers_menu()
        choice = input("Select: ").strip()

        if choice == "0":
            return

        if choice == "1":
            text = input("Plain text: ")
            n = ask_int("Shift (n): ")
            lang = choose_lang(text, ask_lang())
            print("\nResult:", caesar_encrypt(text, n, lang))
            pause()

        elif choice == "2":
            text = input("Cipher text: ")
            n = ask_int("Shift (n): ")
            lang = choose_lang(text, ask_lang())
            print("\nResult:", caesar_decrypt(text, n, lang))
            pause()

        elif choice == "3":
            text = input("Cipher text: ")
            lang = choose_lang(text, ask_lang())
            variants = caesar_bruteforce(text, lang)
            print("\nVariants:")
            for v in variants:
                print(v)
            pause()

        elif choice == "4":
            text = input("Text (EN): ")
            print("\nResult:", rot13(text))
            pause()

        elif choice == "5":
            text = input("Text: ")
            lang = choose_lang(text, ask_lang())
            print("\nResult:", atbash_transform(text, lang))
            pause()

        elif choice == "6":
            text = input("Plain text: ")
            lang = choose_lang(text, ask_lang())
            a = ask_int("a: ")
            b = ask_int("b: ")
            print("\nResult:", affine_encrypt(text, a, b, lang))
            pause()

        elif choice == "7":
            text = input("Cipher text: ")
            lang = choose_lang(text, ask_lang())
            a = ask_int("a: ")
            b = ask_int("b: ")
            print("\nResult:", affine_decrypt(text, a, b, lang))
            pause()

        elif choice == "8":
            text = input("Plain text: ")
            lang = choose_lang(text, ask_lang())
            key = input("Substitution key (alphabet mapping): ").strip()
            print("\nResult:", substitution_encrypt(text, key, lang))
            pause()

        elif choice == "9":
            text = input("Cipher text: ")
            lang = choose_lang(text, ask_lang())
            key = input("Substitution key (alphabet mapping): ").strip()
            print("\nResult:", substitution_decrypt(text, key, lang))
            pause()

        elif choice == "10":
            text = input("Plain text: ")
            key = input("Key: ")
            key_type = input("key_type (text/hex) [text]: ").strip().lower() or "text"
            print("\nCipher hex:", xor_encrypt(text, key, key_type=key_type))
            pause()

        elif choice == "11":
            cipher_hex = input("Cipher hex: ")
            key = input("Key: ")
            key_type = input("key_type (text/hex) [text]: ").strip().lower() or "text"
            print("\nPlain:", xor_decrypt(cipher_hex, key, key_type=key_type))
            pause()

        elif choice == "12":
            text = input("Plain text: ")
            key = input("Key (word): ")
            lang = choose_lang(text + key, ask_lang())
            print("\nResult:", vigenere_encrypt(text, key, lang))
            pause()

        elif choice == "13":
            text = input("Cipher text: ")
            key = input("Key (word): ")
            lang = choose_lang(text + key, ask_lang())
            print("\nResult:", vigenere_decrypt(text, key, lang))
            pause()


        else:
            print("No such option.")


def run_codecs():
    while True:
        show_codecs_menu()
        choice = input("Select: ").strip()

        if choice == "0":
            return

        inp = input("Input: ")

        if choice == "1":
            print("\nResult:", base64_encode(inp))
            pause()
        elif choice == "2":
            print("\nResult:", base64_decode(inp))
            pause()
        elif choice == "3":
            print("\nResult:", base32_encode(inp))
            pause()
        elif choice == "4":
            print("\nResult:", base32_decode(inp))
            pause()
        elif choice == "5":
            print("\nResult:", hex_encode(inp))
            pause()
        elif choice == "6":
            print("\nResult:", hex_decode(inp))
            pause()
        elif choice == "7":
            print("\nResult:", binary_encode(inp))
            pause()
        elif choice == "8":
            print("\nResult:", binary_decode(inp))
            pause()
        else:
            print("No such option.")


def main():
    print(BANNER)
    print("Version: 1.0\n")

    while True:
        show_main_menu()
        choice = input("Select: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            safe_run(run_ciphers)
        elif choice == "2":
            safe_run(run_codecs)
        elif choice == "3":
            safe_run(run_analyzer)
        else:
            print("No such option.")


if __name__ == "__main__":
    main()
