from numpy import isclose


def similar(x, y):
    if (x == 0 or x is None) and (y == 0 or y is None):
        return True
    elif not y:
        return False
    else:
        return isclose(x / y, 1., rtol=1e-04, atol=1e-06)
