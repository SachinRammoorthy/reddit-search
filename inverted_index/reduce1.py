#!/usr/bin/env python3
"""Reduce 1."""
import sys
import itertools


def main():
    """Divide sorted lines into groups that share a key."""
    freq = {}
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        freq[key] = reduce_one_group(group)
    for key, word_dict in freq.items():
        for doc_id, num_occurrences in word_dict.items():
            new_key = key + " " + doc_id
            new_val = str(num_occurrences) + " " + str(len(word_dict))
            print(new_key + "\t" + new_val)


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def reduce_one_group(group):
    """Reduce one group."""
    word_freq = {}
    for line in group:
        doc_id = line.split()[1]
        if doc_id in word_freq:
            word_freq[doc_id] += 1
        else:
            word_freq[doc_id] = 1
    return word_freq


if __name__ == "__main__":
    main()
