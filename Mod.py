# Build on top of code from http://anh.cs.luc.edu/331/code/mod_arith.py

from xgcd import xgcd


class AnyMod:  # for backward compatibility
    """common super class for all Mod classes, so there is a named ancestor."""
    pass


class Mod(AnyMod):  # AnyMod is for backwards compatibility
    """
    A class for modular arithmetic, mod m.
    If m is prime, the inverse() method and division operation are always
    defined, and the class represents a field.
    """

    # class invariant:
    #  self.m is the modulus
    #  self.value is the usual smallest non-negative representative

    def __init__(self, n=0, m=None):
        """
        Construct a Mod object.
        If n is a Mod, just copy its n and m, and any m parameter should match.
        If m is a Mod, take its m value.
        Otherwise both m and n should be integers, m > 1; construct n mod m.
        """
        if isinstance(m, Mod):
            m = m.m
        if isinstance(n, Mod):
            assert m is None or m == n.m, 'moduli do not match'
            self.value = n.value
            self.m = n.m
            return
        else:
            assert isinstance(m, int), 'Modulus type must be int or Mod.'
            assert m > 1, 'Need modulus > 1'
        assert isinstance(n, int), 'Representative value must be int.'
        self.m = m
        self.value = n % m

    def is_residue(self):
        """Return whether the square root of the number exists."""
        if self ** ((self.m - 1) >> 1) == 1:
            return True  # Legendre says 1.
        if self == 0:
            return True  # 0 always has a square root even if it technically isn't a residue.
        return False  # Legendre says -1.

    def sqrt(self):
        """A direct application of Tonelli-Shanks algorithm. Returns a tuple of both roots"""
        assert self.is_residue(), 'Square roots can only be taken for quadratic residues.'
        if self.value == 0:
            sqrt = Mod(0, self.m)
            return sqrt, -sqrt
        if self.m == 2:
            sqrt = Mod(2, self.m)
            return sqrt, -sqrt
        if self.m & 0b11 == 3:
            sqrt = self ** ((self.m + 1) >> 2)
            return sqrt, -sqrt

        # Reduce all the powers of 2 from p - 1.
        s = self.m - 1
        e = 0
        while s & 1 == 0:
            s = s >> 1
            e += 1

        # Find some 'n' with a legendre symbol n|p = -1.
        temp = self.value
        self.value = 2
        while self.is_residue():
            self.value += 1
        n = self.value
        self.value = temp

        # Read the paper "Square roots from 1; 24, 51, 10 to Dan Shanks"
        # by Ezra Brown for more information.

        # x is a guess of the square root that gets better with each iteration.
        # b is the "fudge factor" - by how much we're off with the guess.
        # The invariant x^2 = ab (mod p) is maintained throughout the loop.
        # g is used for successive powers of n to update both a and b.
        # r is the exponent - decreases with each update
        x = pow(self.value, (s + 1) >> 1, self.m)
        b = pow(self.value, s, self.m)
        g = pow(n, s, self.m)
        r = e
        while True:
            t = b
            m = 0
            for m in range(r):
                if t == 1:
                    break
                t = pow(t, 2, self.m)
            if m == 0:
                sqrt = Mod(x, self.m)
                return sqrt, -sqrt
            gs = pow(g, 2 ** (r - m - 1), self.m)
            g = (gs * gs) % self.m
            x = (x * gs) % self.m
            b = (b * g) % self.m
            r = m

    def __str__(self):  # used by str built-in function, which is used by print
        """Return an informal string representation of object"""
        return f"{self.value}"

    def __repr__(self):  # used by repr built-in function
        """Return a formal string representation, usable in the Shell"""
        return f"{self.value}"

    def same_param(self, other):
        """True if other is a Mod with same modulus"""
        return isinstance(other, Mod) and other.m == self.m

    def __add__(self, other):  # used by + infix operand
        """Return self + other, if defined"""
        other = try_like(other, self)
        if other is None:
            return NotImplemented
        return Mod(self.value + other.value, self.m)

    def __sub__(self, other):  # used by - infix operand
        """Return self - other, if defined"""
        other = try_like(other, self)
        if other is None:
            return NotImplemented
        return Mod(self.value - other.value, self.m)

    def __neg__(self):  # used by - unary operand
        """Return -self"""
        return Mod(-self.value, self.m)

    def __mul__(self, other):  # used by * infix operand
        """Return self * other, if defined"""
        other = try_like(other, self)
        if other is None:
            return NotImplemented
        return Mod(self.value * other.value, self.m)

    def __truediv__(self, other):
        """Return self/other if other.inverse() is defined."""
        other = try_like(other, self)
        if other is None:
            return NotImplemented
        return self * other.inverse()

    def __eq__(self, other):  # used by == infix operand
        """Return self == other, if defined
        Allow conversion of int to same Mod type before test.  Good idea?"""
        other = try_like(other, self)
        if other is None:
            return NotImplemented
        return other.value == self.value

    def __ne__(self, other):  # used by != infix operand
        """Return self != other, if defined"""
        return not self == other

    # operations where only the second operand is a Mod (prefix r)
    def __radd__(self, other):
        """Return other + self, if defined, when other is not a Mod"""
        return self + other  # commutative, and now Mod first

    def __rsub__(self, other):
        """Return other - self, if defined, when other is not a Mod"""
        return -self + other  # can make definite Mod first

    def __rmul__(self, other):
        """Return other * self, if defined, when other is not a Mod"""
        return self * other  # commutative, and now Mod first

    def __rdiv__(self, other):
        """Return other/self if self.inverse() is defined."""
        return self.inverse() * other  # can make definite Mod first

    def __pow__(self, n):  # used by ** infix operator
        """
        Compute power using successive squaring for integer n
        Negative n allowed if self has an inverse.
        """
        s = self  # s holds the current square
        if n < 0:
            s = s.inverse()
            n = abs(n)
        return Mod(pow(s.value, n, s.m), s.m)

    def __int__(self):
        """Return lowest non-negative integer representative."""
        return self.value

    def __nonzero__(self):
        """
        Returns True if the current value is nonzero.
        (Used for conversion to boolean.)
        """
        return self.value != 0

    def __hash__(self):
        """ Hash value definition needed for use in dictionaries and sets."""
        return hash(self.value)

    def modulus(self):
        """Return the modulus."""
        return self.m

    def inverse(self):
        """Return the multiplicative inverse or else raise a ValueError."""
        (g, x, y) = xgcd(self.value, self.m)
        if g == 1:
            return Mod(x, self.m)
        raise ValueError("Value not invertible.")


def like(val, model):
    """
    Convert val to a the same kind of object as model.
    This is useful where the underlying class of model has parameters
    making different objects of the same type incompatible.  The assumption
    is that model has a method sameParam, that checks this.
    """
    if model.same_param(val):
        return val  # Avoid unnecessary copy
    return model.__class__(val, model)


def try_like(val, model):
    """
    Convert val to the same kind of object as model, with the same
    required parameters, if possible, or return None
    """
    try:
        return like(val, model)
    except:
        return None
