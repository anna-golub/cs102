package main

import (
    "fmt"
    "flag"
    "os"
    "main/rsa"
    //"main/vigenere"
    //"main/caesar"
)


func main() {
  //ciphertext := caesar.EncryptCaesar("python", 3)
  //fmt.Println("Encrypted message:", ciphertext)

  //plaintext := caesar.DecryptCaesar("SBWKRQ", 3)
  //fmt.Println("Decrypted message:", plaintext)
  
  //ciphertext = vigenere.EncryptVigenere("ATTACKATDAWN", "LEMON")
  //fmt.Println("Encrypted message:", ciphertext)

  //plaintext = vigenere.DecryptVigenere("LXFOPVEFRNHR", "LEMON")
  //fmt.Println("Decrypted message:", plaintext)

  p := flag.Int("p", 11, "")
  q := flag.Int("q", 17, "")
  plaintext := flag.String("text", "something", "")
  flag.Parse()
  keys, err := rsa.GenerateKeypair(*p, *q)
  if err != nil {
      fmt.Println(err)
      os.Exit(1)
  }
  ciphertext := rsa.Encrypt(keys.Private, *plaintext)
  fmt.Println("Encrypted message:", ciphertext)
  fmt.Println("Decrypted message:", rsa.Decrypt(keys.Public, ciphertext))
}