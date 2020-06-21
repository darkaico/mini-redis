
def is_integer(value):
    try:
        int(value)
    except (TypeError, ValueError):
        return False

    return True


def is_float(value):
    try:
        float(value)
    except (TypeError, ValueError):
        return False

    return True
