def try_for_int(n: str):
    try:
        int(n)
        return int(n)
    except ValueError:
        try:
            int(n, 16)
            return int(n, 16)
        except ValueError:
            raise ValueError("Input is not in the correct format for try_for_int.")


def try_for_float(n: str):
    try:
        float(n)
        return float(n)
    except ValueError:
        raise ValueError("Input is not in the correct format for try_for_float.")
