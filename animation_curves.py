import cfg


def jumping_curve(x, y):
    curve = ((x - 12) * (x - 12)) + y - 144
    return curve


def hitting_curve(x):
    return 100 - abs(10 * x - 80)
