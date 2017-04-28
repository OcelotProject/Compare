from .. import cache
from flask import url_for


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


def add_urls_if_needed():
    """Add URLs to model run output datasets if not present"""
    ds = next(iter(cache.run.values()))
    if 'url' not in ds:
        for ds in cache.run.values():
            ds['url'] = url_for(
                'detail',
                name=ds['name'],
                product=ds['reference product'],
                location=ds['location']
            )
            ds['log_url'] = url_for(
                'log_detail',
                name=ds['name'],
                product=ds['reference product'],
                location=ds['location']
            )
