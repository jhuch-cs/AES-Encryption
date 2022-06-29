from aes import Aes 
from byte import Byte
from util import *

import sys

key_string = ""
content_string = ""
options = []
if (len(sys.argv) == 1):
    content_string = input("Content: ")
    key_string = input("Key: ")
    should_encrypt = input("Encrypt [y/n]: ")
    should_decrypt = input("Decrypt [y/n]: ")
    if (should_decrypt.lower() == "y"):
        options.append("--decrypt")
    if (should_encrypt.lower() == "y"):
        options.append("--encrypt")
    print()
elif (len(sys.argv) == 2 or len(sys.argv) > 5):
    print("python3 main.py <hex_content: [a-f0-9]> <key: [a-f0-9]> --encrypt --decrypt")
    exit()
else:
    content_string = sys.argv[1]
    key_string = sys.argv[2]
    options = sys.argv[3:]

key     = [Byte(int(key_string[i:i + 2], 16)) for i in range(0, len(key_string), 2)]
content = [Byte(int(content_string[i:i + 2], 16)) for i in range(0, len(content_string), 2)]

my_aes = Aes(len(key) * 8, key)

if ("--encrypt" in options):
    cipher_text = my_aes.cipher(content)
    print("Encrypted: " + to_hex_from_bytes(cipher_text) + "\n\n")

if ("--decrypt" in options):
    plain_text = my_aes.decipher(content)
    print("Decrypted: " + to_hex_from_bytes(plain_text))