from .. import cache
from .indices import similarity_index


def missing_given():
    for k, v in cache.run.items():
        if k not in cache.given:
            yield v


def missing_model():
    for k, v in cache.given.items():
        if k not in cache.run and v['name'] != "electricity, high voltage, production mix":
            yield v


def in_both():
    for k, v in cache.given.items():
        if k in cache.run:
            v['similarity'] = similarity_index(v, cache.run[k])
            yield v
