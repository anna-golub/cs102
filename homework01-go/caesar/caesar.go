package caesar

func EncryptCaesar(plaintext string, shift int) string {
	var ciphertext string

	for _, ch := range plaintext {
		if (ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z') {
			if (ch+rune(shift) > 'Z' && ch <= 'Z') || (ch+rune(shift) > 'z') {
				ch = ch - 26
			}
			ciphertext += string(ch + rune(shift))
		} else {
			ciphertext += string(ch)
		}
	}

	return ciphertext
}

func DecryptCaesar(ciphertext string, shift int) string {
	var plaintext string

	for _, ch := range ciphertext {
		if (ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z') {
			if (ch-rune(shift) < 'a' && ch >= 'a') || (ch-rune(shift) < 'A') {
				ch = ch + 26
			}
			plaintext += string(ch - rune(shift))
		} else {
			plaintext += string(ch)
		}
	}

	return plaintext
}
