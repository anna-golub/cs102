def encrypt_caesar(plaintext: str) -> str:
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ''
    for ch in plaintext:

        if not ch.isalpha():
            ciphertext += ch
        elif 'x' <= ch <= 'z' or 'X' <= ch <= 'Z':
            ciphertext += chr(ord(ch) - 23)
        else:
            ciphertext += chr(ord(ch) + 3)

    return ciphertext


def decrypt_caesar(ciphertext: str) -> str:
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ''
    for ch in ciphertext:

        if not ch.isalpha():
            plaintext += ch
        elif 'A' <= ch <= 'C' or 'a' <= ch <= 'c':
            plaintext += chr(ord(ch) + 23)
        else:
            plaintext += chr(ord(ch) - 3)

    return plaintext
