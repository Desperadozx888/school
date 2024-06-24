# This is a sample Python script.
import string


def encrypt(plaintext, key):
    alphabet = string.ascii_uppercase
    ciphertext = ""
    n = 1
    for char in plaintext:
        if char.isalpha():
            keystream = (pow(key, 2) + n) % 26
            key = keystream
            index = (alphabet.index(char) + keystream) % 26
            ciphertext += alphabet[index]
            n += 1

        else:
            ciphertext += char
    return ciphertext


def decrypt(ciphertext, key):
    alphabet = string.ascii_uppercase
    plaintext = ""
    counter = 1
    for char in ciphertext:
        if char.isalpha():
            n = counter
            keystream = (pow(key, 2) + n) % 26
            key = keystream
            index = ((alphabet.index(char) - keystream) % 26)
            plaintext += alphabet[index]
            counter += 1
        else:
            plaintext += char
    return plaintext


if __name__ == '__main__':
    message = "I LOVE WOLLONGONG"
    key = 3
    ctext = "MQJJ"
    ciphertext = encrypt(message, key)
    print("Encrypt the message 'I LOVE WOLLONGONG' with key = 3")
    print("Ciphertext: " + ciphertext)
    ptext = decrypt(ciphertext, key)
    print(f"decrypted {ciphertext} : {ptext}")

    plaintext = decrypt(ctext, key)
    print("Decrypt the ciphertext 'MQJJ' with key = 3.")
    print("Plaintext: ", plaintext)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
