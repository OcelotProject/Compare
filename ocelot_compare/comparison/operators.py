from .. import cache
from .indices import similarity_index
import numpy as np


def missing_given():
    for k, v in cache.run.items():
        if k not in cache.given:
            yield v


def missing_model():
    for k, v in cache.given.items():
        if k not in cache.run and v['name'] != "electricity, high voltage, production mix":
            yield v


def in_both():
    for k, v in cache.run.items():
        if k in cache.given:
            v['similarity'] = similarity_index(v, cache.given[k])
            yield v


def calculate_similarities():
    data = []
    for k, v in cache.run.items():
        if k in cache.given:
            similarity = similarity_index(v, cache.given[k])
            v['similarity'] = similarity
            data.append(similarity)

    cache.similarity = np.average(data)
