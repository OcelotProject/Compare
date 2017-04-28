from . import cache
from .comparison import *
from .filesystem import load_detailed_log
from flask import Flask, render_template
import os


static = os.path.join(os.path.dirname(__file__), "web", "static")
templates = os.path.join(os.path.dirname(__file__), "web", "templates")
app = Flask("oc", static_folder=static, template_folder=templates)


@app.route("/")
def index():
    if not (cache.given and cache.run):
        raise ValueError("Must populate given reference and run caches first")
    add_urls_if_needed()
    kwargs = {
        "hv_production": skipped_high_voltage_production_mixes(),
        "missing_given": missing_given(),
        "missing_model": missing_model(),
        "in_both": in_both(),
    }
    return render_template("index.html", **kwargs)

@app.route("/detail/<name>/<product>/<location>/")
def detail(name, product, location):
    model = cache.run[(name, product, location)]
    given = cache.given.get((name, product, location))
    return render_template('detail.html', given=given, model=model)

@app.route("/log/<name>/<product>/<location>/")
def log_detail(name, product, location):
    ds = cache.run.get((name, product, location))
    if not ds:
        404
    filename = os.path.basename(ds['filepath'])
    messages = (line for line in load_detailed_log(cache.run_id)
                if line['dataset']['filename'] == filename)

    return render_template('log_detail.html', ds=ds, messages=messages)
