from input import *
from Algorithm import secp256k1, ECDSA


def main() -> int:
    print("Type a password you want to generate a key from:")
    password = input()
    alg = ECDSA(secp256k1, password)
    print(f"Your private key is {alg.kpriv} and the respective public key is {represent_point(alg.kpub)}.")
    while True:
        print("Type a message you want to sign (or type exit to exit):")
        message = input()
        if message == 'exit':
            break
        signature = alg.sign(message)
        print(f"The signature is r = {signature[0]}, s = {signature[1]}.")
        print(f"Verifying the signature yields: {alg.verify(message, signature)}")
    return 0


if __name__ == "__main__":
    main()
