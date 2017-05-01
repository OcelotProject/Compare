import numpy as np


def consolidate(lst):
    results = []
    for x, y in lst:
        if x:
            if y:
                results.append((x[0], x[1], np.isclose(x[2], y[2]), x[2], y[2], x[3], x[4]))
            else:
                results.append((x[0], x[1], False, x[2], 0, x[3], x[4]))
        else:
            results.append((y[0], y[1], False, 0, y[2], y[3], y[4]))
    return results


def compare_exchanges(first, second):
    exchanges = lambda x: sorted([(e['name'], e.get('subcategory', ''), e['amount'], e['unit'], e['type'])
                                  for e in x['exchanges']])

    results = []
    first, second = exchanges(first), exchanges(second)
    candidate_f, candidate_s = None, None

    while first or second:
        if not candidate_f:
            if first:
                candidate_f = first.pop(0)
            else:
                candidate_f = None
        if not candidate_s:
            if second:
                candidate_s = second.pop(0)
            else:
                candidate_s = None

        if candidate_f and candidate_s:
            if (candidate_f[0] == candidate_s[0]) and  (candidate_f[1] == candidate_s[1]):
                results.append((candidate_f, candidate_s))
                candidate_f, candidate_s = None, None
            elif candidate_f < candidate_s:
                results.append((candidate_f, None))
                candidate_f = None
            else:
                results.append((None, candidate_s))
                candidate_s = None
        elif candidate_f:
            results.append((candidate_f, None))
        else:
            results.append((None, candidate_s))
    return consolidate(results)
