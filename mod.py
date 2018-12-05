# Reused from http://anh.cs.luc.edu/331/code/mod_arith.py

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
        if self.value ** ((self.m - 1) / 2) != 1:
            return False
        return True

    def __str__(self):  # used by str built-in function, which is used by print
        """Return an informal string representation of object"""
        return f"{self.value}"

    def __repr__(self):  # used by repr built-in function
        """Return a formal string representation, usable in the Shell"""
        return f"Mod({self.value}, {self.m})"

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
        # # algorithm (but not in C):
        # result = Mod(1, self.m)
        # while n > 0:
        #    if n % 2 == 1:
        #       result = s * result
        #    s = s * s  # compute the next square
        #    n = n//2    # compute the next quotient
        # return result

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
