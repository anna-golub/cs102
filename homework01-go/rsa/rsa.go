package rsa

import (
	"errors"
	"fmt"
	"math"
	"math/big"
	"math/rand"
)

type Key struct {
	key int
	n   int
}

type KeyPair struct {
	Private Key
	Public  Key
}

func isPrime(n int) bool {
	if (n == 1) || (n != 2 && n%2 == 0) {
		return false
	}
	d := 3
	for d*d <= n {
		if n%d == 0 {
			return false
		}
		d += 2
	}
	return true
}

func gcd(a int, b int) int {
	for a*b != 0 {
		if a > b {
			a %= b
		} else {
			b %= a
		}
	}
	return a + b
}

func multiplicativeInverse(e int, phi int) int {
	var r0, a0, b0, r1, a1, b1, r2, a2, b2 int

	r0 = e % phi
	a0 = 1
	b0 = -(e / phi)

	r1 = phi % r0
	a1 = -(phi / r0)
	b1 = 1 + (e/phi)*(phi/r0)
	r2 = -1

	if r1 == 0 {
		return r0
	}

	for r2 != 0 {
		if r2 == 0 {
			fmt.Println("What the hell!?")
		}

		a2 = a0 - a1*(r0/r1)
		b2 = b0 - b1*(r0/r1)
		r2 = a2*e + b2*phi

		r0 = r1
		r1 = r2
		a0 = a1
		a1 = a2
		b0 = b1
		b1 = b2
	}

	if a0 < 0 {
		a0 += phi * (int(math.Abs(float64(a0)))/phi + 1)
	}
	return a0
}

func GenerateKeypair(p int, q int) (KeyPair, error) {
	if !isPrime(p) || !isPrime(q) {
		return KeyPair{}, errors.New("Both numbers must be prime.")
	} else if p == q {
		return KeyPair{}, errors.New("p and q can't be equal.")
	}

	n := p * q
	phi := (p - 1) * (q - 1)

	e := rand.Intn(phi-1) + 1
	g := gcd(e, phi)
	for g != 1 {
		e = rand.Intn(phi-1) + 1
		g = gcd(e, phi)
	}

	d := multiplicativeInverse(e, phi)
	return KeyPair{Key{e, n}, Key{d, n}}, nil
}

func Encrypt(pk Key, plaintext string) []int {
	cipher := []int{}
	n := new(big.Int)
	for _, ch := range plaintext {
		n = new(big.Int).Exp(
			big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
		n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
		cipher = append(cipher, int(n.Int64()))
	}
	return cipher
}

func Decrypt(pk Key, cipher []int) string {
	plaintext := ""
	n := new(big.Int)
	for _, ch := range cipher {
		n = new(big.Int).Exp(
			big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
		n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
		plaintext += string(rune(int(n.Int64())))
	}
	return plaintext
}
