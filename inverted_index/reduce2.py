#!/usr/bin/env python3
"""Reduce 0."""
import sys
import itertools
import math


def main():
    """Divide sorted lines into groups that share a key."""
    num_posts = 0
    with open('total_document_count.txt', "r", encoding='UTF-8') as line_in:
        num_posts = float(line_in.readline())
    
    calculations = []
    weight_per_doc = {}

    for _, group in itertools.groupby(sys.stdin, keyfunc):
        for _, group2 in itertools.groupby(list(group), keyfunc_middle):
            all_lines = []
            for line in group2:
                values = line.strip().split()
                n_k = values[4]
                id_fk = math.log((num_posts/float(n_k)), 10)
                w_ik = float(values[3]) * float(id_fk)
                all_lines.append([values[1], id_fk, values[2], values[3]])
                if values[2] in weight_per_doc:
                    weight_per_doc[values[2]] += (w_ik ** 2)
                else:
                    weight_per_doc[values[2]] = (w_ik ** 2)
            calculations.append(all_lines)

    for list_of_word_calcs in calculations:
        to_print = (list_of_word_calcs[0][0] + " " +
                    str(list_of_word_calcs[0][1]) + " ")
        for calculation in list_of_word_calcs:
            to_print += (str(calculation[2]) + " " + str(calculation[3]) + " "
                         + str(weight_per_doc[calculation[2]]) + " ")
        to_print = to_print[:-1]
        print(to_print)


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.split("\t")[0]


def keyfunc_middle(line):
    return line.split("\t")[1].split()[0]


if __name__ == "__main__":
    main()
