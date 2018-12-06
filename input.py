from tries import try_for_int, try_for_float
from typing import List, Union
from Curve import O, Point


def parse_input() -> List[str]:
    return input().split()


def read_point(inputs: List[str]) -> Point:
    x = inputs.pop(0)
    if x == 'O':
        return O
    try:
        float(x)
    except ValueError:
        raise ValueError("Input is not in the correct format for read_point.")
    y = inputs.pop(0)
    try:
        float(y)
    except ValueError:
        raise ValueError("Input is not in the correct format for read_point.")
    p = (float(x), float(y))
    return p


def read_int(inputs: List[str]) -> int:
    n = inputs.pop(0)
    return try_for_int(n)


def read_number(inputs: List[str]) -> Union[float, int]:
    n = inputs.pop(0)
    if '.' in n:
        return try_for_float(n)
    return try_for_int(n)

