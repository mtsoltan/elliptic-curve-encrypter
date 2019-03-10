from hashlib import sha256
from os import urandom
from typing import Dict, Tuple
from Curve import Curve
from Mod import Mod

Signature = Tuple[int, int]

secp256k1 = {  # Certicom secp256-k1
    'P': 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,  # 256 bit field prime.
    'A': 0,  # 256 bit curve A paramter
    'B': 7,  # 256 bit curve B paramter
    'Gx': 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,  # 256 bit base point x coord.
    'Gy': 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,  # 256 bit base point y coord.
    # N is the smallest positive integer such that N * G = O
    'N': 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,  # 256 bit order of base point.
}

nist256p = {
    'P': 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff,
    'A': -3,
    'B': 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b,
    'Gx': 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
    'Gy': 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5,
    'N': 115792089210356248762697446949407573529996955224135760342422259061068512044369,
}

nist384p = {
    'P':  (1 << 384) - (1 << 128) - (1 << 96) + (1 << 32) - 1,
    'A': -3,
    'B': 0xb3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875ac656398d8a2ed19d2a85c8edd3ec2aef,
    'Gx': 0xaa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7,
    'Gy': 0x3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f,
    'N': 39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942643,
}

nist521p = {
    'P': (2 << 520) - 1,
    'A': -3,
    'B': 0x051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00,
    'Gx': 0xc6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66,
    'Gy': 0x11839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650,
    'N': 6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449,
}


class ECDSA:
    ALPHANUM = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    BASE = len(ALPHANUM)  # 58

    def __init__(self, paramters: Dict, password: str):
        """
        Initializes the algorithm with the specified paramters.
        """
        self.D = paramters
        self.curve = Curve(self.D['A'], self.D['B'], self.D['P'])
        self.G = (Mod(self.D['Gx'], self.D['P']), Mod(self.D['Gy'], self.D['P']))
        self.N = self.D['N']
        self.kpriv = self.intsha256(password)
        self.kpub = self.curve.multiply(self.G, self.kpriv)

    @staticmethod
    def intsha256(text: str) -> int:
        return int(sha256(text.encode('utf-8')).hexdigest(), 16)

    @staticmethod
    def random_number(blen: int) -> int:  # len is in bits
        """
        Returns cryptographically secure random numbers, unlike the built-in random() of python.
        """
        blen = (blen & 111) + (blen >> 3)  # Divide by 8 and round up.
        rv = 0
        for e in urandom(blen):
            rv += e
            rv <<= 8
        return rv & ((1 << blen) - 1)

    def b58encode(self, v):  # TODO: This isn't used as of now. Will be used soon, change to base64 encoding.
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

    def sign(self, message: str, k: int = None) -> Signature:
        if k is None:
            k: int = self.random_number(255)  # TODO: HMAC Generation from hash of message in some RFC algorithm class.
        if k > self.N:  # Random number generation is constructed in such a way that this is impossible.
            return self.sign(message)  # But we can't always assume that RNG won't change.
        r: Mod = Mod(self.curve.multiply(self.G, k)[0].value, self.N)  # Reduction modulo N is important.
        if r == 0:  # A computationally impossible but theoretically possible case. WARNING: Mod to int comparison.
            return self.sign(message)
        t1: Mod = self.intsha256(message) + self.kpriv * r
        s: Mod = Mod(k, self.N).inverse() * t1.value
        if s == 0:  # Again, computationally impossible but theoretically possible. WARNING: Mod to int comparison.
            return self.sign(message)
        assert isinstance(r, Mod) and isinstance(s, Mod), "Signature final values have to be Mods."
        return r.value, s.value

    def verify(self, message: str, signature: Signature) -> bool:
        r, s = signature
        if r > self.N - 1 or r < 1:
            return False
        if s > self.N - 1 or s < 1:
            return False
        inv: Mod = Mod(s, self.N).inverse()  # Conversion to Mod happens here. r is still int.
        u1: Mod = inv * self.intsha256(message)
        u2: Mod = inv * r
        x: Mod = self.curve.add(self.curve.multiply(self.G, u1.value), self.curve.multiply(self.kpub, u2.value))[0]
        if x.value == r:
            return True
        return False
