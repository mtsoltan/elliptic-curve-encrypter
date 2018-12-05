# TODO: Implement multiplication (irreversible trapdoor function).
from typing import Tuple, Union, Optional

from mod import Mod

Point = Union[Tuple[Union[float, Mod], Union[float, Mod]], bool]
ModularPoint = Union[Tuple[Mod, Mod], bool]
O: Point = False  # Point at infinity.

P_secp265k1 = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F"  # 256 bits field prime.
A_secp265k1 = 0
B_secp265k1 = 7
G_secp265k1 = "0279BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798"  # 264 bits base point (Gx, Gy).
N_secp265k1 = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141"  # 256 bits order of base point.
H_secp265k1 = 1  # The cofactor of base point.

"""
Rules:
Kpub = Kpriv x G
Private keys are randomly generated, usually iterative operation of a cryptographic hash function to a password.
Hash functions are designed in such a way to provide a bitstream of sufficient length to form a key.

G is used as the generator for public keys. Multiplication is straightforward through the double-and-add method.
Private keys cannot be recreated since multiplication is irreversible.

For a fixed set of paramters T = (P, A, B, G, N, H), to sign a message, m (ECDSA):
1- Randomly generate Kpriv (int), and generate Kpub = Kpriv x G (point).
2- Select a random integer k, 1 < k <= N - 1.
3- Compute r = (k * G).x mod N
   * where multiplication is over the elliptic curve (A, B, P)
   * where if r == 0 go to step 1.
4- Compute inv(k) using xgcd, and SHA1(m) as a 160-bit integer.
5- Compue s = inv(k) * (SHA1(m) + Kpriv * r) mod N
   * where if s == 0 go to step 1.
6- The signature is (r, s).

To verify the signature (r, s) given Kpub:
1- Verify that r, s are integers in the interval [1, n - 1]
2- Compute inv(s) using xgcd, and SHA1(m) as a 160-bit integer.
3- Compute u1 = inv(s) * SHA1(m) mod N and u2 = inv(s) * r mod N
4- Compute x = (u1 * G + u2 * Kpub).x mod N.
5- Accept if x == r.
"""


class Curve:
    def __init__(self, a: Union[int, float], b: Union[int, float], p: Optional[int]=None):
        """
        Initializes the curve, y**2 = x**3 + a*x + b taking into
        account whether it is over a finite or an infinite field.
        """
        self.A = a
        self.B = b
        self.P = int(p)
        if self.P:
            self.A = Mod(int(self.A), self.P)
            self.B = Mod(int(self.B), self.P)
            self.G = 0  # TODO: Lookup generators.
        else:
            self.A = float(self.A)
            self.B = float(self.B)

    def find(self, p: ModularPoint) -> bool:
        """
        Finds whether the point p lies on this curve.
        """
        if self.P is None:
            raise ValueError("This function can only be used on a finite field curve.")
        return p[0] ** 3 + p[0] * self.A + self.B == p[1] ** 2

    def modulate(self, p: Point) -> ModularPoint:
        """
        Makes sure that the point p is modulo P and lies on the finite field curve E(Fp)(x, y)
        If it isn't modulo P, it is changed to be modulo P.
        """
        if self.P is None:
            raise ValueError('This function can only be used on a finite field curve.')
        rv = O if p == O else (Mod(int(p[0]), self.P), Mod(int(p[1]), self.P))
        if not self.find(rv):
            raise ValueError(f"The point ({p[0]}, {p[1]}) was not found on the finite field curve.")
        return rv

    def add(self, p1: Point, p2: Point) -> Point:
        """
        Algorithm on P.285 for adding points on elliptic curves.
        """
        if self.P:
            p1 = self.modulate(p1)
            p2 = self.modulate(p2)
        if p1 == O:
            return p2
        if p2 == O:
            return p1
        x1, y1 = p1
        x2, y2 = p2
        if x1 == x2 and y1 == -y2:
            return O
        if x1 == x2 and y1 == y2:
            l: Union[float, Mod] = (3 * x1 ** 2 + self.A) / (2 * y1)
        else:
            l: Union[float, Mod] = (y2 - y1) / (x2 - x1)
        x3 = l ** 2 - x1 - x2
        y3 = l * (x1 - x3) - y1
        p3 = (x3, y3)
        return self.modulate(p3) if self.P else p3

    def multiply(self, p: Point, k: int) -> Point:
        """
        Double-and-add algorithm as described on wikipedia.
        """
        if self.P:
            p = self.modulate(p)
        n = p
        q = O
        while k > 0:
            if k & 1:
                q = self.add(q, n)
            n = self.add(q, q)
            k >>= 1
        return q
