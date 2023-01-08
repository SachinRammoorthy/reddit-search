#!/usr/bin/env python3
"""Map 2."""
import sys

for line in sys.stdin:
    els = line.split("\t")
    doc_id = els[0].split()[1]
    KEY = str(hash(doc_id) % 3)
    val = (els[0].split()[0] + " " + els[0].split()[1] + " " +
           els[1].split()[0] + " " + els[1].strip().split()[1])
    print(KEY + "\t" + val)
