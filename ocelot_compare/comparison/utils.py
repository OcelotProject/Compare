from .. import cache
from urllib.parse import urlparse, quote


def prepare_loaded_data():
    print("Preparing data for comparisons")
    add_given_reference_product()
    cache.given = convert_to_dict(cache.given)
    cache.run = convert_to_dict(cache.run)
    add_exchange_names_activities()
    add_locations()
    add_filepaths()


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


def add_exchange_names_activities():
    mapping = {x['id']: x['name'] for x in cache.given.values()}
    for ds in cache.given.values():
        for exc in ds['exchanges']:
            if 'technosphere' in exc['type']:
                try:
                    exc['activity'] = mapping[exc['activity link']]
                except KeyError:
                    exc['activity'] = ''
            elif exc['type'] == 'reference product':
                exc['activity'] = ds['name']

    a_mapping = {x['code']: x['name'] for x in cache.run.values()}
    f_mapping = {x['code']: x['reference product'] for x in cache.run.values()}
    for ds in cache.run.values():
        for exc in ds['exchanges']:
            if 'technosphere' in exc['type']:
                try:
                    exc['activity'] = a_mapping[exc['code']]
                    exc['name'] = f_mapping[exc['code']]
                except KeyError:
                    exc['activity'] = ''
            elif exc['type'] == 'reference product':
                exc['activity'] = ds['name']


def convert_to_dict(lst):
    return {(o['name'], o['reference product'], o['location']): o
            for o in lst}


def add_urls_if_needed(url):
    """Add URLs to model run output datasets if not present"""
    ds = next(iter(cache.run.values()))
    if 'url' not in ds:
        pr = urlparse(url)
        base = pr.scheme + "://" + pr.netloc + "/"

        for ds in cache.run.values():
            ds['url'] = (
                base + 'detail/' + quote(ds['name']) + '/' +
                quote(ds['reference product']) + '/' +
                quote(ds['location']) + '/'
            )
            ds['log_url'] = (
                base + 'log/' + quote(ds['name']) + '/' +
                quote(ds['reference product']) + '/' +
                quote(ds['location']) + '/'
            )
            ds['raw_url'] = (
                base + 'model-raw/' + quote(ds['name']) + '/' +
                quote(ds['reference product']) + '/' +
                quote(ds['location']) + '/'
            )
        for ds in cache.given.values():
            ds['raw_url'] = (
                base + 'given-raw/' + quote(ds['name']) + '/' +
                quote(ds['reference product']) + '/' +
                quote(ds['location']) + '/'
            )


def add_locations():
    mapping = {x['code']: x['location'] for x in cache.run.values()}
    for ds in cache.run.values():
        for exc in ds['exchanges']:
            if exc['type'] == 'reference product':
                exc['location'] = ds['location']
                continue
            try:
                exc['location'] = mapping[exc['code']]
            except KeyError:
                exc['location'] = None

    mapping = {x['id']: x['location'] for x in cache.given.values()}
    for ds in cache.given.values():
        for exc in ds['exchanges']:
            if exc['type'] == 'reference product':
                exc['location'] = ds['location']
                continue
            try:
                exc['location'] = mapping[exc['activity link']]
            except KeyError:
                exc['location'] = None

def add_filepaths():
    mapping = {x['code']: x['filepath'] for x in cache.run.values()}
    for ds in cache.run.values():
        for exc in ds['exchanges']:
            if exc['type'] == 'reference product':
                continue
            try:
                exc['filepath'] = mapping[exc['code']]
            except KeyError:
                pass
        for exc in ds.get('suppliers', []):
            try:
                exc['filepath'] = mapping[exc['code']]
            except KeyError:
                pass
