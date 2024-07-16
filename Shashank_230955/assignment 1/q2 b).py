def Dec(m, k):
    decrypt= ''
    for char in m:
            if char.isalpha():
               new_char = chr(((ord(char) - 97 - k) % 26) + 97) if char.islower() else chr(((ord(char) - 65 - k) % 26) + 65)
               decrypt += new_char
            else:
                 decrypt+=char
    return decrypt
def possible_messages(encrypt_message):
    possible_messages = []
    for key in range(1,26):
        possible_messages.append(Dec(encrypt_message, key))
    return possible_messages

message1 = 'bm ptl wtfg xtlr tztbg'
message2 = 'rc fjb mjvw njbh'
print(" probable message 1:",possible_messages(message1))
print(" probable message 2:",possible_messages(message2))