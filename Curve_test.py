from input import *


def main_o_represent_point(p: Point) -> str:
    if p == O:
        return 'O'
    return f"({p[0]}, {p[1]})"


def main_p_do_operation(operation, curve: Curve, inputs: List[str]) -> bool:
    ret = False
    if operation.lower() == 'add':  # Adds two points.
        p1 = read_point(inputs, curve)
        p2 = read_point(inputs, curve)
        p_out = curve.add(p1, p2)
        print(f"The output point is {main_o_represent_point(p_out)}.")
        ret = True
    if operation.lower() == 'mul':  # Multiplies a point by an integer.
        p = read_point(inputs, curve)
        k = read_int(inputs)
        p_out = curve.multiply(p, k)
        print(f"The output point is {main_o_represent_point(p_out)}.")
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


def main_i_curve_parameters() -> Curve:
    try:
        print("Insert space separated values of A B and an optional P: ")
        curve = parse_input()
        a = read_number(curve)
        b = read_number(curve)
        p = read_int(curve) if len(curve) else None
        curve = Curve(a, b, p)
        print(f"Our elliptic curve is x^3 + {curve.A}x + {curve.B}")
        if curve.P:
            print(f" on the prime field with P={curve.P}")
        return curve
    except Exception as e:
        print(e)
        return main_i_curve_parameters()


def main_p_main_loop(curve: Curve) -> bool:
    try:
        print("Insert an operation (add, mul, pts, fiy, exit): ")
        operation = parse_input()
        opcode = operation.pop(0)
        if opcode == 'exit':
            return False
        assert main_p_do_operation(opcode, curve, operation),\
            "The operation given was not understood by the program."
        return True
    except Exception as e:
        print(e)
        return main_p_main_loop(curve)


def main() -> int:
    curve = main_i_curve_parameters()

    while main_p_main_loop(curve):
        continue

    return 0


if __name__ == "__main__":
    main()
