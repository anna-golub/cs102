def message():
    print("Hello, World!")


if __name__ == "__main__":
    message()


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

        elif plaintext[i].isupper():
            ciphertext[i] = chr((ord(plaintext[i]) + ord(keyword[i % len(keyword)])) % 65)
        else:
            ciphertext[i] = chr((ord(plaintext[i]) + ord(keyword[i % len(keyword)])) % 97)

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
    # PUT YOUR CODE HERE
    return plaintext
