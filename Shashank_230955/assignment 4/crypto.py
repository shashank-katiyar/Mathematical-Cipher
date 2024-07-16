from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad,unpad
from base64 import b64encode, b64decode
import os

#working on a  message to check 
# key_pair = RSA.generate(1024)

# pub_key = key_pair.publickey().exportKey()
# priv_key = key_pair.exportKey()

# print(pub_key)
# print(priv_key)
# key = RSA.importKey(pub_key)

# message = b'A message to secure'
# print(message)

# cipher = PKCS1_OAEP.new(key)
# ciphertext = cipher.encrypt(message)
# print(ciphertext)
# key = RSA.importKey(priv_key)
# cipher = PKCS1_OAEP.new(key)

# # we assume the cipher text has been sent and stored in a variable
# decrypted_message = cipher.decrypt(ciphertext)
# print(decrypted_message)


# Generate RSA keys
def generate_rsa_keys():
    key = RSA.generate(2048)
    priv_key = key.export_key()
    pub_key = key.publickey().export_key()
    #RSA keys are multi-line strings of characters, usually stored in .pem files
    with open("private.pem", "wb") as priv_file:
        priv_file.write(priv_key)
    with open("public.pem", "wb") as pub_file:
        pub_file.write(pub_key)
    # print(pub_key)
    # print(priv_key)
    return priv_key, pub_key

def encrypt_aes_key(aes_key, pub_key):
    key = RSA.import_key(pub_key)
    cipher = PKCS1_OAEP.new(key)
    encrypted_aes_key = cipher.encrypt(aes_key)
    return encrypted_aes_key

def decrypt_aes_key(encrypted_aes_key, priv_key):
    key = RSA.import_key(priv_key)
    cipher = PKCS1_OAEP.new(key)
    aes_key = cipher.decrypt(encrypted_aes_key)
    return aes_key

def encrypt_chunk(chunk, aes_key):
    cipher = AES.new(aes_key, AES.MODE_ECB)
    encrypted_chunk = cipher.encrypt(pad(chunk, AES.block_size))
    return encrypted_chunk


def decrypt_chunk(encrypted_chunk, aes_key):
    cipher = AES.new(aes_key, AES.MODE_ECB)
    chunk = unpad(cipher.decrypt(encrypted_chunk), AES.block_size)
    return chunk

def divide_file_into_chunks(file_path, chunk_size):
    with open(file_path, 'rb') as file:
        chunk = file.read(chunk_size)
        while chunk:
            yield chunk
            chunk = file.read(chunk_size)

def encrypt_file(file_path, pub_key):
    aes_key = os.urandom(32)
    encrypted_aes_key = encrypt_aes_key(aes_key, pub_key)
    encrypted_chunks = []
    for chunk in divide_file_into_chunks(file_path, 1024):
        encrypted_chunk = encrypt_chunk(chunk, aes_key)
        encrypted_chunks.append(encrypted_chunk)
    return encrypted_aes_key, encrypted_chunks

def decrypt_file(encrypted_aes_key, encrypted_chunks, priv_key):
    aes_key = decrypt_aes_key(encrypted_aes_key, priv_key)
    decrypted_chunks = []
    for encrypted_chunk in encrypted_chunks:
        decrypted_chunk = decrypt_chunk(encrypted_chunk, aes_key)
        decrypted_chunks.append(decrypted_chunk)
    return decrypted_chunks

def reassemble_file(decrypted_chunks, output_file_path):
    with open(output_file_path, 'wb') as file:
        for chunk in decrypted_chunks:
            file.write(chunk)

priv_key, pub_key = generate_rsa_keys()
file_path = 'text.txt'
encrypted_aes_key, encrypted_chunks = encrypt_file(file_path, pub_key)
decrypted_chunks = decrypt_file(encrypted_aes_key, encrypted_chunks, priv_key)
reassembled_file_path = 'reassembled_file.txt'
reassemble_file(decrypted_chunks, reassembled_file_path)