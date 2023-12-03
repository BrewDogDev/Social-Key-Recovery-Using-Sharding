from Crypto.Cipher import AES

key = b'Sixteen byte key'
def encrypt(data):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return nonce, ciphertext
def decrypt(nonce, ciphertext):
    key = b'Sixteen byte key'
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode()

if __name__ == "__main__":
    data = "123456789,123456789"
    print(data)
    nonce, ciphertext = encrypt(data)
    print(ciphertext)
    plain_text = decrypt(nonce, ciphertext)
    print(plain_text.decode())
