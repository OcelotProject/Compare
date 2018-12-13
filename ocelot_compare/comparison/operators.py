from .. import cache
from .indices import similarity_index, high_voltage_production
import numpy as np
import pyprind


def missing_given():
    for k, v in cache.run.items():
        if k not in cache.given:
            yield v


def missing_model():
    for k, v in cache.given.items():
        if k not in cache.run and not high_voltage_production(v):
            yield v


def in_both():
    for k, v in cache.run.items():
        if k in cache.given:
            v['similarity'] = similarity_index(v, cache.given[k])
            yield v


def calculate_similarities():
    data = []
    for k, v in pyprind.prog_bar(cache.run.items()):
        if k in cache.given:
            similarity = similarity_index(v, cache.given[k])
            v['similarity'] = similarity
            data.append(similarity)

    cache.similarity = np.average(data)
