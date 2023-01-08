"""Main API."""
import re
import math
import flask
import index


@index.app.route('/api/v1/')
def list_services():
    msg = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(msg), 200


@index.app.route('/api/v1/hits/')
def get_hits():
    query = flask.request.args.get('q', type=str)
    query = clean_query(query)
    if len(query) == 0:
        return flask.jsonify({"hits": [], }), 200
    
    term_freq_in_q = {}
    for word in query:
        if word in term_freq_in_q:
            term_freq_in_q[word] += 1
        else:
            term_freq_in_q[word] = 1
    
    inverted_index = index.app.config["INVERTED_INDEX"]
    setlist = []
    index_mapper = {}

    for i, line in enumerate(inverted_index):
        items = line.split()
        if items[0] in query:
            word_arr = []
            index_mapper[items[0]] = i
            curr_i = 2
            while curr_i < len(items):
                word_arr.append(items[curr_i])
                curr_i += 3
            word_arr = set(word_arr)
            setlist.append(word_arr)

    for word in query:
        if word not in index_mapper:
            setlist.append(set())

    docs_w_query = set.intersection(*setlist)
    weight = flask.request.args.get('w', default=0.5, type=float)
    hits = calculate_ordering(docs_w_query,
                           generate_entire_info(index_mapper, docs_w_query),
                           weight, term_freq_in_q)
    hits = sorted(hits, key=lambda x: x["score"], reverse=True)
    msg = {
        "hits": hits,
    }

    return flask.jsonify(msg), 200


def generate_entire_info(index_mapper, docs_w_query):
    entire_info = {}
    inverted_index = index.app.config["INVERTED_INDEX"]

    for word in index_mapper:
        items = inverted_index[index_mapper[word]].strip().split(" ")
        curr_i = 2
        while curr_i < len(items):
            if items[curr_i] in docs_w_query:
                array_to_insert = [items[1], items[curr_i],
                                   items[curr_i+1], items[curr_i+2]]
                if word in entire_info:
                    entire_info[word].append(array_to_insert)
                else:
                    entire_info[word] = [array_to_insert]
            curr_i += 3
    return entire_info


def calculate_ordering(docs_w_query, entire_info, weight, term_freq_in_q):
    hits = []
    entire_info_i = 0

    for _ in docs_w_query:
        doc_vector = []
        q_vector = []
        q_norm_factor = 0
        word_in = ""

        for word in entire_info:
            word_in = word
            q_val_to_add = (float(term_freq_in_q[word])
                            * float(entire_info[word][entire_info_i][0]))
            q_vector.append(q_val_to_add)
            in_1 = float(entire_info[word][entire_info_i][0])
            doc_vector.append(in_1 *
                              float(entire_info[word][entire_info_i][2]))
            q_norm_factor += (q_val_to_add) ** 2
        
        tfidf = dot(doc_vector, q_vector, math.sqrt(float(q_norm_factor)),
                    math.sqrt(float(entire_info[word_in][entire_info_i][3])))

        val = float(index.app.config["PAGERANK"]
                    [entire_info[word_in][entire_info_i][1]])

        hits.append({"postid": entire_info[word_in][entire_info_i][1],
                    "score": float(weight * val + (1 - weight) * tfidf)})

        entire_info_i += 1

    return hits


def clean_query(query):
    stopwords = index.app.config["STOPWORDS"]
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query).casefold()
    terms = query.split()
    terms = [x for x in terms if x not in stopwords]

    return terms


def dot(v_1, v_2, v_3, v_4):
    return sum(x*y for x, y in zip(v_1, v_2))/(v_3 * v_4)
