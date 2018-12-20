from . import cache
from .comparison import *
from .filesystem import load_detailed_log, add_similarity_value
from flask import Flask, render_template, request, abort, url_for
# from json2html import *
from .html_table import json2html
import os


static = os.path.join(os.path.dirname(__file__), "web", "static")
templates = os.path.join(os.path.dirname(__file__), "web", "templates")
app = Flask("oc", static_folder=static, template_folder=templates)


def order_dict(dictionary):
    # https://stackoverflow.com/questions/22721579/sorting-a-nested-ordereddict-by-key-recursively
    return {k: order_dict(v) if isinstance(v, dict) else v
            for k, v in sorted(dictionary.items())}


def prepare_follow_cache():
    for i, instance in enumerate(cache.follow):
        for j, ds in enumerate(instance['datasets']):
            ds['url'] = url_for(".followed_detail", func_index=i, ds_index=j)


@app.route("/compare")
def compare():
    if not (cache.given and cache.run):
        raise ValueError("Must populate given reference and run caches first")

    add_urls_if_needed(request.url)
    if not cache.calculated:
        print("Calculating similarities")
        calculate_similarities()
        cache.calculated = True
    if cache.follow:
        follow = {
            'url': url_for('.followed_index'),
            'name': cache.follow[0]['datasets'][0]['name'],
        }
    else:
        follow = None
    kwargs = {
        "hv_production": skipped_high_voltage_production_mixes(),
        "missing_given": missing_given(),
        "missing_model": missing_model(),
        "in_both": in_both(),
        "similarity": cache.similarity,
        "previous": add_similarity_value(),
        "follow": follow,
    }
    return render_template("index.html", **kwargs)

@app.route("/show")
def show():
    if not cache.run:
        raise ValueError("Must populate run cache first")

    add_urls_if_needed(request.url)
    return render_template("show.html", data=cache.run.values())

@app.route("/detail/<name>/<product>/<location>/")
def detail(name, product, location):
    try:
        model = cache.run[(name, product, location)]
        given = cache.given.get((name, product, location))
    except KeyError:
        abort(404)
    similarity = similarity_index(model, given) if given else None
    exchanges = compare_exchanges(model, given) if given else None
    return render_template('detail.html', given=given, model=model, exchanges=exchanges, similarity=similarity)

@app.route("/log/<name>/<product>/<location>/")
def log_detail(name, product, location):
    try:
        ds = cache.run[(name, product, location)]
    except KeyError:
        abort(404)
    filename = os.path.basename(ds['filepath'])
    messages = (line for line in load_detailed_log(cache.run_id)
                if line['dataset']['filename'] == filename)

    return render_template('log_detail.html', ds=ds, messages=messages)

@app.route("/model-raw/<name>/<product>/<location>/")
def model_raw(name, product, location):
    try:
        ds = cache.run[(name, product, location)]
    except KeyError:
        abort(404)
    return json2html.convert(json=ds, sort=True)

@app.route("/given-raw/<name>/<product>/<location>/")
def given_raw(name, product, location):
    try:
        ds = cache.given[(name, product, location)]
    except KeyError:
        abort(404)
    return json2html.convert(json=ds, sort=True)

@app.route("/followed/")
def followed_index():
    if not cache.follow_prepared:
        prepare_follow_cache()
        cache.follow_prepared = True
    return render_template(
        'follow.html', ds=cache.follow[0], states=cache.follow
    )

@app.route("/followed/<func_index>/<ds_index>/")
def followed_detail(func_index, ds_index):
    func_index, ds_index = int(func_index), int(ds_index)
    ds = cache.follow[func_index]['datasets'][ds_index]
    return render_template(
        'follow_detail.html',
        ds=ds,
        table=json2html.convert(json=ds, sort=True)
    )
