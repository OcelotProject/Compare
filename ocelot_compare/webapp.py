from flask import Flask, render_template
import os


static = os.path.join(os.path.dirname(__file__), "web", "static")
templates = os.path.join(os.path.dirname(__file__), "web", "templates")
app = Flask("oc", static_folder=static, template_folder=templates)


class Cache:
    reference = []
    run = []

cache = Cache()


@app.route("/")
def index():
    print(len(cache.reference), len(cache.run))
    if not (cache.reference and cache.run):
        raise ValueError("Must populate reference and run caches first")
    return render_template("index.html")
