from . import cache
from .comparison import *
from flask import Flask, render_template
import os


static = os.path.join(os.path.dirname(__file__), "web", "static")
templates = os.path.join(os.path.dirname(__file__), "web", "templates")
app = Flask("oc", static_folder=static, template_folder=templates)


@app.route("/")
def index():
    if not (cache.given and cache.run):
        raise ValueError("Must populate given reference and run caches first")
    kwargs = {
        "hv_production": skipped_high_voltage_production_mixes(),
        "missing_given": missing_given(),
        "missing_model": missing_model(),
        "in_both": in_both(),
    }
    return render_template("index.html", **kwargs)
