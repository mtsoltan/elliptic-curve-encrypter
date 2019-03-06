from input import *
from ecdsa import SigningKey, VerifyingKey, SECP256k1, ellipticcurve
from hashlib import sha256
from Algorithm import secp256k1, ECDSA
from Curve import Point


def test_ecdsa() -> int:
    print("Type a password you want to generate a key from:")
    password = input()
    alg = ECDSA(secp256k1, password)
    assert validate_keys(alg.kpriv, alg.kpub), "Exiting because public keys did not match."

    while True:
        print("Type a message you want to sign (or type exit to exit):")
        message = input()
        if message == 'exit':
            break
        # TODO: hash abstraction. Check todo in Algorithm.py
        rnd = alg.random_number(255)  # To make sure both signatures use the same random number.
        signature = alg.sign(message, rnd)
        assert validate_signature(alg.kpriv, message, rnd, signature), "Exiting because signatures did not match."

        print(f"Verifying the signature yields: {alg.verify(message, signature)}")
    return 0


def validate_keys(sk: int, vk: Point) -> bool:
    std_sk = SigningKey.from_secret_exponent(sk, SECP256k1, sha256)
    std_vk = std_sk.get_verifying_key()
    std_point = ellipticcurve.Point(SECP256k1.curve, vk[0].value, vk[1].value)
    std_vk_from_point = VerifyingKey.from_public_point(std_point, SECP256k1, sha256)
    public_keys_match = std_vk_from_point.to_string() == std_vk.to_string()

    print(f"Your private key is {sk} and the respective public key is {represent_point(vk)}.")
    if public_keys_match:
        print(f"This private key generates the same public key using py-ecdsa.")
    else:
        print(f"The public key generated using py-ecdsa is {str(std_vk.pubkey.point)}")

    return public_keys_match


def validate_signature(sk, msg, k, sig):
    def sigencode(r, s, _):
        return r, s
    std_sig = SigningKey.from_secret_exponent(sk, SECP256k1, sha256).sign(bytes(msg, 'utf-8'), None, None, sigencode, k)
    signatures_match = std_sig[0] == sig[0] and std_sig[1] == sig[1]

    print(f"The signature is r = {sig[0]}, s = {sig[1]}.")
    if signatures_match:
        print(f"This signature is the same as the one generated using py-ecdsa.")
    else:
        print(f"The signature generated using py-ecdsa is  r = {std_sig[0]}, s = {std_sig[1]}.")

    return signatures_match


if __name__ == "__main__":
    test_ecdsa()
