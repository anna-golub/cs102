def message():
    print("Hello, World!")

if __name__ == "__main__":
    message()




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

    ciphertext = [''] * len(plaintext)
    for i in range(len(plaintext)):

        if not plaintext[i].isalpha():
            ciphertext[i] = plaintext[i]

        elif plaintext[i] in ('X', 'Y', 'Z', 'x', 'y', 'z'):
            ciphertext[i] = chr(ord(plaintext[i]) - 23)
        else:
            ciphertext[i] = chr(ord(plaintext[i]) + 3)

    return "".join(ciphertext)


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

    plaintext = [''] * len(ciphertext)
    for i in range(len(ciphertext)):

        if not ciphertext[i].isalpha():
            plaintext[i] = ciphertext[i]

        elif ciphertext[i] in ('A', 'B', 'C', 'a', 'b', 'c'):
            plaintext[i] = chr(ord(ciphertext[i]) + 23)
        else:
            plaintext[i] = chr(ord(ciphertext[i]) - 3)

    return "".join(plaintext)
