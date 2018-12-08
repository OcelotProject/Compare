from numpy import isclose
from collections import defaultdict
from itertools import zip_longest


def consolidate(lst):
    results = []
    for x, y in lst:
        if x and y:
            results.append((x[0], x[1], x[2],
                            isclose(x[3], y[3], rtol=1e-04, atol=1e-06),
                            x[3], y[3], x[3] / (y[3] or 1), x[4], x[5]))
        elif x:
                results.append((x[0], x[1], x[2], False, x[3], 0, 0, x[4], x[5]))
        else:
            results.append((y[0], y[1], y[2], False, 0, y[3], 0, y[4], y[5]))
    return results


def compare_exchanges(first, second):
    exchanges = lambda x: sorted([(
        e['name'],
        e.get('activity', ''),
        e.get('location') or e.get('subcompartment', ''),
        e['amount'],
        e['unit'],
        e['type']
    ) for e in x['exchanges']])

    first_exchanges = defaultdict(list)
    for exc in exchanges(first):
        first_exchanges[exc[:3]].append(exc)

    second_exchanges = defaultdict(list)
    for exc in exchanges(second):
        second_exchanges[exc[:3]].append(exc)

    all_keys = sorted(set(first_exchanges).union(set(second_exchanges)))

    results = []
    for key in all_keys:
        for x, y in zip_longest(first_exchanges[key], second_exchanges[key]):
            results.append((x, y))

    return consolidate(results)
