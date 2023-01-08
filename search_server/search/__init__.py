"""Return information.

This takes in two parameters.
"""
import os
import flask

app = flask.Flask(__name__)  # pylint: disable=invalid-name

app.config.from_object('search.config')

import search.views  # noqa: E402 pylint: disable=wrong-import-position
import search.model  # noqa: E402 pylint: disable=wrong-import-position
