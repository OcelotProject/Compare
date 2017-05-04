from numpy import isclose


def consolidate(lst):
    results = []
    for x, y in lst:
        if x:
            if y:
                results.append((x[0], x[1], x[2],
                                isclose(x[3], y[3], rtol=1e-04, atol=1e-06),
                                x[3], y[3], x[4], x[5]))
            else:
                results.append((x[0], x[1], x[2], False, x[3], 0, x[4], x[5]))
        else:
            results.append((y[0], y[1], y[2], False, 0, y[3], y[4], y[5]))
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
            candidate_f = None
        else:
            results.append((None, candidate_s))
            candidate_s = None
    return consolidate(results)
