from . import similar
from .. import cache


def high_voltage_production(ds):
    return 'electricity' in ds['name'] and 'production mix' in ds['name']


def skipped_high_voltage_production_mixes():
    total = 0
    for k, v in cache.given.items():
        if k not in cache.run and high_voltage_production(v):
            total += 1
    return total


def similarity_index(x, y):
    """Calculate a numeric score of how close two datasets are"""
    def as_dict(ds):
        get_key = lambda exc: (exc['name'], exc.get('activity', ''),
                               (exc.get('location') or exc.get('subcompartment', '')))
        return {get_key(exc): exc['amount'] for exc in ds['exchanges']}

    xd, yd = as_dict(x), as_dict(y)
    all_keys = set(xd).union(set(yd))
    try:
        # print("len(all_keys):", len(all_keys))
        # print("similarity values:", [(similar(xd.get(key), yd.get(key)),
        #                               (similar(xd.get(key), yd.get(key)) in (True, "roundoff")),
        #                               xd.get(key), yd.get(key))
        #                              for key in all_keys])
        # print("index:", sum(
        #     similar(xd.get(key), yd.get(key)) in (True, "roundoff")
        #     for key in all_keys
        # ) / len(all_keys))
        return sum(
            similar(xd.get(key), yd.get(key)) in (True, "roundoff", "missing")
            for key in all_keys
        ) / len(all_keys)
    except ZeroDivisionError:
        return -1
