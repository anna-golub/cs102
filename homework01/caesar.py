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

    ciphertext = "".join(ciphertext)
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
    # PUT YOUR CODE HERE
    return plaintext
