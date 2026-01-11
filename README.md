[README.md](https://github.com/user-attachments/files/24551588/README.md)
# CipherLab CLI

**CipherLab** CipherLab is a command-line application for encryption, decryption, and basic cryptanalysis.
The project is inspired by tools like CyberChef, but is implemented in Python.
---

##  English

###  Features

CipherLab includes 3 main modules:

#### 1) Ciphers
- Caesar cipher (ROT N)
- ROT13
- Atbash cipher
- Affine cipher
- Substitution cipher
- XOR cipher (supports `text` and `hex` keys, output in `hex`)
- Vigenère cipher

#### 2) Codecs (Encodings)
- Base64
- Base32
- Hex (Base16)
- Binary

#### 3) Analyzer (Cryptanalysis tools)
Analyzer does **not decode automatically**, but **suggests actions** depending on detected input type.

Supported analysis:
- Automatic format detection:
  - HEX
  - Binary
  - Base64 / Base32
  - Text (possible Caesar/Atbash/Vigenère)
- Caesar brute-force
- XOR brute-force (TOP results by readability score)
- XOR crib attack (known plaintext / partial key recovery)
- Vigenère analysis using:
  - language detection (EN/RU)
  - IC (Index of Coincidence)
  - key length suggestion (top lengths)

---

###  Project Structure

Example structure:

```text
crypto_tool/
├── main.py
├── README.md
├── ciphers/
│   ├── __init__.py
│   ├── caesar_cipher.py
│   ├── atbash_cipher.py
│   ├── affine_cipher.py
│   ├── substitution_cipher.py
│   ├── xor_cipher.py
│   └── vigenere_cipher.py
├── brute_force/
│   ├── __init__.py
│   ├── caesar_bruteforce.py
│   ├── xor_bruteforce.py
│   └── xor_crib.py
├── codecs_lab/
│   ├── __init__.py
│   ├── base64_codec.py
│   ├── base32_codec.py
│   ├── hex_codec.py
│   └── binary_codec.py
└── utils/
    ├── __init__.py
    ├── text_utils.py
    ├── language_utils.py
    └── vigenere_analysis.py
```


---

### How to Run

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 main.py
```

#### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\activate
py main.py
```

---

### 🧠 Educational Goal

CipherLab is designed to help students understand:

- the difference between **encoding vs encryption**
- how classical ciphers work
- why weak algorithms can be broken using brute-force and analysis
- basic cryptanalysis methods (IC, crib attacks, frequency logic)

---

##  Русский

###  Возможности

**CipherLab** — это учебное консольное приложение для **шифрования, дешифрования и анализа данных**.  
Проект выполнен как **итоговый проект 11 класса** и вдохновлён сервисом *CyberChef*, но реализован на Python.

---

###  1) Шифры (Ciphers)
- Шифр Цезаря (ROT N)
- ROT13
- Атбаш
- Аффинный шифр
- Подстановочный шифр
- XOR (ключ в `text` или `hex`, результат в `hex`)
- Шифр Виженера

---

###  2) Кодировки (Codecs)
- Base64
- Base32
- Hex (Base16)
- Binary

---

###  3) Анализатор (Analyzer)
Analyzer **ничего не расшифровывает автоматически**, а **предлагает возможные действия** на основе анализа входной строки.

Поддерживается:
- Автоматическое определение формата:
  - HEX
  - Binary
  - Base64 / Base32
  - Text (возможны Caesar/Atbash/Vigenere)
- Брутфорс шифра Цезаря
- XOR brute-force (ТОП вариантов по оценке читаемости текста)
- XOR crib attack (подбор ключа по известному фрагменту текста)
- Анализ Виженера:
  - автоопределение языка (EN/RU)
  - IC (Index of Coincidence / индекс совпадений)
  - предположение длины ключа

---

### ️ Как запустить

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 main.py
```

#### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\activate
py main.py
```

---
