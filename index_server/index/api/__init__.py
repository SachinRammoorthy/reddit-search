"""Index API."""
import csv
from pathlib import Path
import index.api.main
import index.config
import index


def load_index():
    """Return information.

    This takes in two parameters.
    """
    in_path = Path("index_server/index/stopwords.txt")
    with open(in_path, 'r', encoding='UTF-8') as file_in:
        stopwords = set(line.strip() for line in file_in.readlines())
    pagerank = {}
    in_path_2 = Path("index_server/index/pagerank.out")
    with open(in_path_2, 'r', encoding='UTF-8') as f_i:
        reader = csv.reader(f_i)
        pagerank = {rows[0]: rows[1] for rows in reader}
    param = index.app.config['INDEX_PATH']
    path = Path(f"index_server/index/inverted_index/{param}")
    with open(path, encoding='UTF-8') as invert_in:
        inverted_index = invert_in.readlines()
    return stopwords, pagerank, inverted_index
