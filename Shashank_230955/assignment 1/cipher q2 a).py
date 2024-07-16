def Enc(m,k):
    encrypt=""
    for char in m:
          if char.islower():
               new_char = chr(((ord(char) - 97 + k) % 26) + 97)  
               encrypt+=new_char
          elif char.isupper():
               new_char= chr(((ord(char) - 65 + k) % 26) + 65)
               encrypt+=new_char
          else:
               encrypt+=char
    return encrypt
m1 = 'iitk is better than iitd and iitb'
k1 = 9
encrypted_message1 = Enc(m1, k1)
print("Encrypted message 1:", encrypted_message1)

m2 = 'lets learn cryptography'
k2 = 25
encrypted_message2 = Enc(m2, k2)
print("Encrypted message 2:", encrypted_message2)
 