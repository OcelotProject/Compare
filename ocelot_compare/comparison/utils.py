from .. import cache

def prepare_loaded_data():
    print("Preparing data for comparisons")
    add_given_reference_product()
    cache.given = convert_to_dict(cache.given)
    cache.run = convert_to_dict(cache.run)


def add_given_reference_product():
    for ds in cache.given:
        if "reference product" not in ds:
            rps = [exc
                   for exc in ds['exchanges']
                   if exc['type'] == 'reference product'
                   and exc['amount']
            ]
            if not len(rps) == 1:
                raise ValueError("Unallocated dataset:", ds['filepath'])
        ds['reference product'] = rps[0]['name']


def convert_to_dict(lst):
    return {(o['name'], o['reference product'], o['location']): o
            for o in lst}
