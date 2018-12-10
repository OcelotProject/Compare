from .. import cache
from .similar import similar


def skipped_high_voltage_production_mixes():
    total = 0
    for k, v in cache.given.items():
        if k not in cache.run and v['name'] == "electricity, high voltage, production mix":
            total += 1
    return total


def similarity_index(x, y):
    """Calculate a numeric score of how close two datasets are"""
    def as_dict(lst):
        d = {}
        for exc in lst['exchanges']:
            key = (exc['name'], exc.get('subcompartment'))
            d[key] = d.get(key, 0) + exc['amount']
        return d

    xd, yd = as_dict(x), as_dict(y)
    try:
        return sum(
            similar(v, yd.get(k))
            for k, v in xd.items()
        ) / len(xd)
    except ZeroDivisionError:
        return -1
