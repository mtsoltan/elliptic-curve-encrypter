from typing import Tuple, Union, Optional
from Mod import Mod

Coordinate = Union[float, Mod]
IntableCoordinate = Union[float, int, Mod]
Point = Union[Tuple[Coordinate, Coordinate], bool]
ModularPoint = Union[Tuple[Mod, Mod], bool]
O: Point = False  # Point at infinity.


class Curve:
    def __init__(self, a: IntableCoordinate, b: IntableCoordinate, p: Optional[int]):
        """
        Initializes the curve, y**2 = x**3 + a*x + b taking into
        account whether it is over a finite or an infinite field.
        """
        self.A = a
        self.B = b
        self.P = p
        assert p is None or (isinstance(a, (int, Mod)) and isinstance(b, (int, Mod))),\
            "Finite field curves can only have integer values of a and b."
        if self.P:
            assert isinstance(p, int), "Only integer values of p are allowed."
            self.P = int(p)
            self.A = Mod(self.A, self.P)
            self.B = Mod(self.B, self.P)
        else:
            self.A = float(self.A)
            self.B = float(self.B)

    def find(self, p: Point) -> bool:
        """
        Finds whether the point p lies on this curve.
        """
        if p == O:
            return True
        if self.P:
            assert isinstance(p[0], (Mod, int)) and isinstance(p[1], (Mod, int)),\
                "Only modular points can be found on a finite field curve."
            p = (Mod(p[0], self.P), Mod(p[1], self.P))
        return p[0] ** 3 + p[0] * self.A + self.B == p[1] ** 2

    def find_y(self, x: IntableCoordinate) -> Point:  # Both y values so technically a tuple.
        """
        Finds whether the point p lies on this curve.
        """
        if self.P is None:
            y = (x ** 3 + x * self.A + self.B) ** 0.5
            return y, -y
        assert isinstance(x, (int, Mod)), "Finite field curves cannot have a non-integer coordinate."
        return Mod(x ** 3 + x * self.A + self.B, self.P).sqrt()

    def list_points(self):
        """
        WARNING: ONLY USE THIS FOR SMALL CURVES.
        Loops over all possible x coordinates in the field, and finds out y values if they exist.
        Returns a set of all possible coordinates on the curve.
        """
        if self.P is None:
            raise ValueError('This function can only be used on a finite field curve.')
        rv = []
        for x in range(self.P):
            try:
                y1, y2 = self.find_y(x)
                x = Mod(x, self.P)
                rv.append((x, y1))
                rv.append((x, y2))
            except AssertionError:
                continue
        return rv

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
            n = self.add(n, n)
            k >>= 1
        return q
