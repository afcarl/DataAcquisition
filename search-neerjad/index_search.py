from collections import defaultdict  # https://docs.python.org/2/library/collections.html

from words import get_text, words


def create_index(files):
    """
    Given a list of fully-qualified filenames, build an index from word
    to set of document IDs. A document ID is just the index into the
    files parameter (indexed from 0) to get the file name. Make sure that
    you are mapping a word to a set of doc IDs, not a list.
    For each word w in file i, add i to the set of document IDs containing w
    Return a dict object mapping a word to a set of doc IDs.
    """
    document_ID = {}
    index = {}
    for i in range(0, len(files)):
        document_ID[files[i]] = i
    terms = []

    for file in files:
        terms = get_text(file)
        terms = words(terms)
        for term in terms:
            if index.__contains__(term) == True:
                index[term].add(document_ID[file])

            else :
                index[term] = {document_ID[file]}
    return index

def index_search(files, index, terms):
    """
    Given an index and a list of fully-qualified filenames, return a list of
    doc IDs whose file contents has all words in terms parameter as normalized
    by your words() function.  Parameter terms is a list of strings.
    You can only use the index to find matching files; you cannot open the files
    and look inside.
    """
    file_list = [None] * len(terms)
    for i in range(0,len(terms)):
        if index.__contains__(terms[i]):
            file_list[i] = index[terms[i]]
        else:
            return None
    result = set.intersection(*file_list)
    result_files = []
    for r in result:
        result_files.append(files[r])
    return result_files