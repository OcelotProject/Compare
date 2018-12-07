#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Ocelot-compare CLI interface.

Usage:
  ocelot-compare compare <run_id> <ref_dirpath> [--debug]
  ocelot-compare show <run_id> [--debug]

Options:
  --list             List the updates needed, but don't do anything
  -h --help          Show this screen.
  --version          Show version.

"""
from docopt import docopt
from ocelot_compare import cache
from ocelot_compare.comparison import prepare_loaded_data
from ocelot_compare.filesystem import (
    load_model_run,
    load_cached_datasets,
    create_reference_result,
)
from ocelot_compare.webapp import app
import threading
import webbrowser


def run_flask_app(host="127.0.0.1", port="5000", debug=False, loc='compare'):
    url = "http://{}:{}/{}".format(host, port, loc)
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
            cache.run_id = args['<run_id>']
            cache.run = load_model_run(cache.run_id)
            if args['compare']:
                try:
                    cache.given = load_cached_datasets(args['<ref_dirpath>'])
                except AssertionError:
                    create_reference_result(args['<ref_dirpath>'])
                    cache.given = load_cached_datasets(args['<ref_dirpath>'])

        prepare_loaded_data()
        if args['compare']:
            loc = 'compare'
        elif args['show']:
            loc = 'show'
        run_flask_app(loc=loc, debug=args['--debug'])
    except KeyboardInterrupt:
        print("Terminating Ocelot comparison interface")
        sys.exit(1)


if __name__ == "__main__":
    main()
