def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = [''] * len(plaintext)

    for i in range(len(plaintext)):
        if not plaintext[i].isalpha():
            ciphertext[i] = plaintext[i]
        else:
            plainind = 65
            if ord(plaintext[i]) >= 97:
                plainind = 97
            keyind = 65
            if ord(keyword[i % len(keyword)]) >= 97:
                keyind = 97

            ciphertext[i] = chr(
                (ord(plaintext[i]) % plainind + ord(keyword[i % len(keyword)]) % keyind) % 26 + plainind)

    ciphertext = "".join(ciphertext)

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = [''] * len(ciphertext)
    for i in range(len(ciphertext)):

        if not ciphertext[i].isalpha():
            plaintext[i] = ciphertext[i]
        else:
            cipherind = 65
            if ord(ciphertext[i]) >= 97:
                cipherind = 97
            keyind = 65
            if ord(keyword[i % len(keyword)]) >= 97:
                keyind = 97

            plaintext[i] = chr(
                (ord(ciphertext[i]) % cipherind - ord(keyword[i % len(keyword)]) % keyind) % 26 + cipherind)

    plaintext = "".join(plaintext)
    return plaintext
