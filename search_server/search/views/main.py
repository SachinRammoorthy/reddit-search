"""Return information.

This takes in two parameters.
"""
import threading
import requests
import flask
import search


@search.app.route('/', methods=['GET'])
def show_index():
    """Return information.

    This takes in two parameters.
    """
    # Connect to database
    connection = search.model.get_db()

    query = flask.request.args.get('q', None)
    weight = flask.request.args.get('w', 0.5)

    if not query:
        return flask.render_template("index.html")
    res = []

    # make calls to all three index servers concurrently
    # merge results from all three and sort
    # query database for top 10 results and display

    thread_1 = threading.Thread(target=lambda: q_i(0, query, weight, res))
    thread_1.start()

    thread_2 = threading.Thread(target=lambda: q_i(1, query, weight, res))
    thread_2.start()

    thread_3 = threading.Thread(target=lambda: q_i(2, query, weight, res))
    thread_3.start()

    thread_1.join()
    thread_2.join()
    thread_3.join()

    res.sort(key=lambda x: x["score"], reverse=True)
    res = res[:min(10, len(res))]

    ret = {"feed": []}

    def find_nth(haystack, needle, n):
        start = haystack.find(needle)
        while start >= 0 and n > 1:
            start = haystack.find(needle, start+len(needle))
            n -= 1
        return start

    for hit in res:
        cur = connection.execute(
            "SELECT title, summary, score, url "
            f"FROM Posts WHERE postid='{hit['postid']}'"
        )
        info = cur.fetchone()
        if info["summary"] == "...":
            info["summary"] = "No summary available"
        if info["url"] == "":
            info["url"] = "No url available"
        info["title"] = info["title"].capitalize()
        info["subreddit"] = info["url"][:find_nth(info["url"], "/", 3)]
        ret["feed"].append(info)

    ret["query"] = query
    ret["weight"] = weight
    res = []

    return flask.render_template("results.html", **ret)


def q_i(num, query, weight, res):
    """Return info."""
    url = search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"][num]
    url += ("?q=" + query + "&w=" + str(weight))
    resp = requests.get(url, timeout=3)

    for hit in resp.json()["hits"]:
        res.append(hit)
