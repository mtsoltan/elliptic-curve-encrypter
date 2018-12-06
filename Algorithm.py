"""
import ecdsa
import base64
hashlib.sha256(data).digest()
"""
import hashlib
from os import urandom
from typing import Dict
from Curve import Curve
from Mod import Mod


secp256k1 = {
    'P': 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,  # 256 bit field prime.
    'A': 0,  # 256 bit curve A paramter
    'B': 7,  # 256 bit curve B paramter
    'Gx': 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,  # 256 bit base point x coord.
    'Gy': 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,  # 256 bit base point y coord.
    # N is the smallest positive integer such that N * G = O
    'N': 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,  # 256 bit order of base point.
    # H is the ratio between the curve order #E(Fp) and the base point order n.
    'H': 1   # The cofactor of base point.
}


class Algorithm:
    ALPHANUM = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    BASE = len(ALPHANUM)  # 58

    def __init__(self, paramters: Dict, password: str):
        """
        Initializes the algorithm with the specified paramters.
        """
        self.D = paramters
        self.curve = Curve(self.D['A'], self.D['B'], self.D['P'])
        self.G = (Mod(self.D['Gx'], self.D['P']), Mod(self.D['Gy'], self.D['P']))
        self.kpriv = self.int2xsha256(password)
        self.kpub = self.curve.multiply(self.G, self.kpriv)

    @staticmethod
    def int2xsha256(text: str) -> int:
        return int(hashlib.sha256(hashlib.sha256(text).digest()).hexdigest(), 16)

    @staticmethod
    def random_number(blen: int) -> int:  # len is in bits
        blen = (blen & 111) + (blen >> 3)  # Divide by 8 and round up.
        ord_array = map(ord, urandom(blen))
        rv = 0
        for e in ord_array:
            rv += e
            rv <<= 8
        return rv & ((1 << blen) - 1)

    def b58encode(self, v):
        """
        Encodes v, which is a string of bytes, to base58.
        """
        long_value = 0
        for (i, c) in enumerate(v[::-1]):
            long_value += (256**i) * ord(c)
        result = ''
        while long_value >= self.BASE:
            div, mod = divmod(long_value, self.BASE)
            result = self.ALPHANUM[mod] + result
            long_value = div
        result = self.ALPHANUM[long_value] + result

        # Bitcoin does a little leading-zero-compression:
        # leading 0-bytes in the input become leading-1s
        n_pad = 0
        for c in v:
            if c == '\0':
                n_pad += 1
            else:
                break
        return self.ALPHANUM[0] * n_pad + result

    def sign(self, message: str) -> str:
        return ''

    def verify(self, message: str, signature: str) -> bool:
        return False
