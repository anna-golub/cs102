go test -v main/caesar
=== RUN   TestEncryptCaesar
--- PASS: TestEncryptCaesar (0.00s)
=== RUN   TestDecryptCaesar
--- PASS: TestDecryptCaesar (0.00s)
PASS
ok      main/caesar 0.037s

go test -v main/vigenere
=== RUN   TestEncryptVigenere
--- PASS: TestEncryptVigenere (0.00s)
=== RUN   TestDecryptVigenere
--- PASS: TestDecryptVigenere (0.00s)
PASS
ok      main/vigenere   0.032s

go test -v main/rsa
=== RUN   TestIsPrime
--- PASS: TestIsPrime (0.00s)=== RUN   TestGCD
--- PASS: TestGCD (0.00s)
=== RUN   TestMultiplicativeInverse
--- PASS: TestMultiplicativeInverse (0.00s)
=== RUN   TestEncrypt
--- PASS: TestEncrypt (0.00s)
=== RUN   TestDecrypt
--- PASS: TestDecrypt (0.00s)
PASS
ok      main/rsa    0.010s