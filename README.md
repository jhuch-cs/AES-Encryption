## What is this? ##
A python implementation of AES-128, AES-192 and AES-256

## Non-cryptographically Secure! ##
This is not a hardened implementation of AES! This project was a way for me to understand how the algorithm works and is not intended
for real world use.

## How to Run ##
`python3 main.py <plaintext: [a-f0-9]> <key: [a-f0-9]> --encrypt --decrypt`

Use `--encrypt` to encrypt and `--decrypt` to decrypt. The command line parsing isn't super robust, but both
`python3 main.py` and `python3 main.py deadbeefdeadbeefdeadbeefdeadbeef deadbeefdeadbeefdeadbeefdeadbeef --encrypt --decrypt` should work. 

Make sure your `python3` version is somewhat up-to-date as string interpolation is a Python 3.6+ feature.