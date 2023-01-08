"""Index API."""
import os
import flask

app = flask.Flask(__name__)  # pylint: disable=invalid-name

app.config.from_object('index.config')

app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")

import index.api  # noqa: E402 pylint: disable=wrong-import-position

# Load inverted index, stopwords, and pagerank into memory
SW = "STOPWORDS"
PR = "PAGERANK"
II = "INVERTED_INDEX"
app.config[SW], app.config[PR], app.config[II] = index.api.load_index()
