# import sys
from curve import Curve, O, Point, ModularPoint
from typing import List


def parse_input() -> List[str]:
    return input().split()


def read_point(inputs: List[str]):
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


def read_int(inputs: List[str]):
    n = inputs.pop(0)
    try:
        int(n)
    except ValueError:
        raise ValueError("Input is not in the correct format for read_int.")
    return n


def do_operation(operation, curve: Curve, inputs: List[str]) -> bool:
    ret = False
    if operation.lower() == 'add':
        p1 = read_point(inputs)
        p2 = read_point(inputs)
        p_out = curve.add(p1, p2)
        print(f"The output point is ({p_out[0]}, {p_out[1]}).")
        ret = True
    if operation.lower() == 'mul':
        p = read_point(inputs)
        k = read_int(inputs)
        p_out = curve.multiply(p, k)
        print(f"The output point is ({p_out[0]}, {p_out[1]}).")
        ret = True
    return ret


def main() -> int:
    print("Insert space separated values of A B and an optional P: ")
    curve = parse_input()
    curve = Curve(float(curve[0]), float(curve[1]), curve[2] if curve[2] else None)
    print(f"Our elliptic curve is x^3 + {curve.A}x + {curve.B}")
    if curve.P:
        print(f" on the prime field with P={curve.P}")

    s = 1  # Initial value for the while.
    while s:
        print("Insert an operation or press enter to exit: ")
        operation = parse_input()
        s = len(operation)
        op = operation.pop(0)
        if not do_operation(op, curve, operation):
            print("The operation given was not understood by the program.")
    return 0


if __name__== "__main__" :
    main()