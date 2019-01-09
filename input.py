from tries import try_for_int, try_for_number
from typing import List, Union
from Curve import O, Point, Curve


def represent_point(p: Point) -> str:
    if p == O:
        return 'O'
    return f"({p[0]}, {p[1]})"


def parse_input() -> List[str]:
    return input().split()


def read_point(inputs: List[str], curve: Curve) -> Point:
    x = inputs.pop(0)
    if x == 'O':
        return O
    x = try_for_number(x)
    y = inputs.pop(0)
    y = try_for_number(y)
    p = (x, y)
    assert curve.find(p), "The point we are trying to read in read_point was not found on the curve."
    if curve.P:
        return curve.modulate(p)
    return p


def read_int(inputs: List[str]) -> int:
    n = inputs.pop(0)
    return try_for_int(n)


def read_number(inputs: List[str]) -> Union[float, int]:
    n = inputs.pop(0)
    return try_for_number(n)

