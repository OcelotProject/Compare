#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Ocelot-compare CLI interface.

Usage:
  compare-cli <run_id> <ref_dirpath>

Options:
  --list             List the updates needed, but don't do anything
  -h --help          Show this screen.
  --version          Show version.

"""
from docopt import docopt
from ocelot_compare.webapp import app, cache
from ocelot_compare.filesystem import (
    load_model_run,
    load_cached_datasets,
    create_reference_result,
)
import threading
import webbrowser


def run_flask_app(host="127.0.0.1", port="5000", debug=True):
    url = "http://{}:{}".format(host, port)
    threading.Timer(1., lambda: webbrowser.open_new_tab(url)).start()
    app.run(
        debug=debug,
        host=host,
        port=int(port)
    )


def main():
    try:
        args = docopt(__doc__, version='Ocelot comparison interface 0.1')

        if not cache.run:
            print("Loading results")
            cache.run = load_model_run(args['<run_id>'])
            try:
                cache.reference = load_cached_datasets(args['<ref_dirpath>'])
            except AssertionError:
                create_reference_result(args['<ref_dirpath>'])
                cache.reference = load_cached_datasets(args['<ref_dirpath>'])

        run_flask_app()
    except KeyboardInterrupt:
        print("Terminating Ocelot comparison interface")
        sys.exit(1)


if __name__ == "__main__":
    main()
