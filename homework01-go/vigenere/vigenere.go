package vigenere

func EncryptVigenere(plaintext string, keyword string) string {
	var ciphertext string

	for i, ch := range plaintext {
		key := rune(keyword[i%len(keyword)])
		if key < 97 {
			key -= 65
		} else {
			key -= 97
		}

		if (ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z') {
			if (ch+key > 'Z' && ch <= 'Z') || (ch+key > 'z') {
				ch = ch - 26
			}
			ciphertext += string(ch + key)
		} else {
			ciphertext += string(ch)
		}
	}

	return ciphertext
}

func DecryptVigenere(ciphertext string, keyword string) string {
	var plaintext string
	var ch_const rune

	for i, ch := range ciphertext {
		key := rune(keyword[i%len(keyword)])
		if key < 97 {
			key -= 65
		} else {
			key -= 97
		}

		if (ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z') {
			if ch >= 'A' && ch <= 'Z' {
				ch_const = 65
			} else {
				ch_const = 97
			}
			ch -= ch_const

			if ch-key < 0 {
				ch = ch + 26
			}
			plaintext += string(ch - key + ch_const)
		} else {
			plaintext += string(ch)
		}
	}

	return plaintext
}
