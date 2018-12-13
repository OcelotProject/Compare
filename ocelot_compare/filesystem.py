from . import cache
from ocelot.filesystem import __io_version__
from ocelot.io import extract_directory
import appdirs
import datetime
import hashlib
import json
import os
import pickle


def ocelot_base_dir():
    """Return Ocelot cache and output data directory path."""
    return appdirs.user_data_dir("Ocelot", "ocelot_project")


def cache_for_data_dir(data_path, io_version=None):
    """Get file path for cached data"""
    return os.path.join(
        ocelot_base_dir(),
        "cache",
        hashlib.md5(
            (os.path.abspath(data_path) +
             (io_version or __io_version__)).encode("utf-8")
        ).hexdigest() + ".pickle"
    )


def load_cached_datasets(data_path, io_version=None):
    """Return the cached datasets for source directory ``data_path``."""
    fp = cache_for_data_dir(data_path, io_version)
    assert os.path.isfile(fp), "Can't find cached data"
    with open(fp, "rb") as f:
        return pickle.load(f)


def load_last_compare():
    """Get filepath to last comparison data directory"""
    fp = os.path.join(ocelot_base_dir(), "config.json")
    try:
        config = json.load(open(fp))
    except:
        config = {}
    return config['last_compare_path']


def save_last_compare(path):
    """Save filepath for last comparison data directory"""
    fp = os.path.join(ocelot_base_dir(), "config.json")
    try:
        config = json.load(open(fp))
    except:
        config = {}
    config['last_compare_path'] = os.path.abspath(path)
    with open(fp, "w") as f:
        json.dump(config, f)


def add_similarity_value():
    fp = os.path.join(ocelot_base_dir(), "config.json")
    try:
        config = json.load(open(fp))
    except:
        config = {}
    similarities = config.get('similarities', [])
    found = {x[0] for x in similarities}
    if cache.run_id not in found:
        config['similarities'] = (
            [(cache.run_id, cache.similarity, datetime.datetime.now().isoformat())] +
            similarities[:9]
        )
    with open(fp, "w") as f:
        json.dump(config, f)
    return similarities


def load_model_run(run_id):
    """Return the model run data"""
    fp = os.path.join(
        ocelot_base_dir(),
        "model-runs",
        run_id,
        "final-results.pickle"
    )
    assert os.path.isfile(fp), "Can't find this model run"
    with open(fp, "rb") as f:
        return pickle.load(f)


def load_detailed_log(run_id):
    """Return the model run data"""
    fp = os.path.join(
        ocelot_base_dir(),
        "model-runs",
        run_id,
        "detailed.log.json"
    )
    assert os.path.isfile(fp), "Can't find detailed log file"
    for line in open(fp, encoding='utf-8'):
        yield json.loads(line)


def create_reference_result(data_path, use_mp=True):
    """Extract and save known result for database"""
    fp = cache_for_data_dir(data_path)
    if os.path.isfile(fp):
        return
    extract_directory(data_path, use_mp=use_mp)
    return fp
