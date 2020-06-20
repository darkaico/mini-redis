
def is_integer(value):
    try:
        int(value)
    except (TypeError, ValueError):
        return False

    return True
