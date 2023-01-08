#!/usr/bin/env python3
"""Map 1."""
import sys
import re

with open('stopwords.txt', 'r', encoding='UTF-8') as thing_in:
    stopwords = set(line.strip() for line in thing_in.readlines())

for line in sys.stdin:
    elements = line.split(",")
    doc_id = elements[0][1:-1]

    doc_body = line[len(doc_id)+4:].replace(',', ' ')

    doc_body = re.sub(r"[^a-zA-Z0-9 ]+", "", doc_body).casefold()

    terms = doc_body.split()
    terms = [x for x in terms if x not in stopwords]

    for term in terms:
        print(term + "\t" + doc_id)
