from Curve import Curve
from input import *


def repr_point(p: Point) -> str:
    if p == O:
        return 'O'
    return f"({p[0]}, {p[1]})"


def do_operation(operation, curve: Curve, inputs: List[str]) -> bool:
    ret = False
    if operation.lower() == 'add':  # Adds two points.
        p1 = read_point(inputs)
        p2 = read_point(inputs)
        p_out = curve.add(p1, p2)
        print(f"The output point is {repr_point(p_out)}.")
        ret = True
    if operation.lower() == 'mul':  # Multiplies a point by an integer.
        p = read_point(inputs)
        k = read_int(inputs)
        p_out = curve.multiply(p, k)
        print(f"The output point is {repr_point(p_out)}.")
        ret = True
    if operation.lower() == 'fiy':  # Finds y given x.
        x = read_int(inputs)
        y_out = curve.find_y(x)
        print(f"The values of y for the given x is {y_out[0].value} and {y_out[1].value}.")
        ret = True
    if operation.lower() == 'pts':  # Lists all points
        print(f"The possible points in this curve for this field are:\n{curve.list_points()}")
        ret = True
    return ret


def main() -> int:
    print("Insert space separated values of A B and an optional P: ")
    curve = parse_input()
    a = read_number(curve)
    b = read_number(curve)
    p = read_number(curve) if len(curve) else None
    curve = Curve(a, b, p)
    print(f"Our elliptic curve is x^3 + {curve.A}x + {curve.B}")
    if curve.P:
        print(f" on the prime field with P={curve.P}")

    while True:
        print("Insert an operation (add, mul, pts, fiy, exit): ")
        operation = parse_input()
        s = len(operation)
        opcode = operation.pop(0)
        if opcode == 'exit':
            break
        if not do_operation(opcode, curve, operation):
            print("The operation given was not understood by the program.")
    return 0


if __name__ == "__main__":
    main()
