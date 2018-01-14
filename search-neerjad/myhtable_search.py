# Got slate magazine data from http://www.anc.org/data/oanc/contents/
# rm'd .xml, .anc files, leaving just .txt
# 4534 files in like 55 subdirs

from htable import *
from words import get_text, words
import pandas as pd


def myhtable_create_index(files):
    """
    Build an index from word to set of document indexes
    This does the exact same thing as create_index() except that it uses
    your htable.  As a number of htable buckets, use 4011.
    Returns a list-of-buckets hashtable representation.
    """
    nbuckets = 4011
    table = htable(nbuckets)
    for value in range(0, len(files)):
        terms = get_text(files[value])
        terms = words(terms)
        for key in terms:
            table = htable_put(table, key, {value})

    return table

def myhtable_index_search(files, index, terms):
    """
    This does the exact same thing as index_search() except that it uses your htable.
    I.e., use htable_get(index, w) not index[w].
    """
    result = []
    for i in range(0, len(terms)):
        result.append(htable_get(index, terms[i]))

    if result.__contains__(None):
    #if result == [None] * len(terms):
        return None
    else:
        result = set.intersection(*result)
        result_files = []
        for r in result:
            result_files.append(files[r])
        return result_files
