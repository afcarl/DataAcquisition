import sys
import re
import nltk
from nltk.stem.porter import *
from sklearn.feature_extraction import stop_words
import xml.etree.cElementTree as ET
from collections import Counter
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import zipfile
import os
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


PARTIALS = False

def gettext(xmltext):
    """
    Parse xmltext and return the text from <title> and <text> tags
    """
    xmltext = xmltext.encode('ascii', 'ignore')  # ensure there are no weird char
    tree = ET.ElementTree(ET.fromstring(xmltext))
    combined_text = ''
    for elem in tree.iter('title'):
        combined_text = combined_text + elem.text

    for elem in tree.iterfind('.//text/*'):
        combined_text = combined_text + ' ' + elem.text
    return combined_text

def tokenize(text):
    """
    Tokenize text and return a non-unique list of tokenized words
    found in the text. Normalize to lowercase, strip punctuation,
    remove stop words, drop words of length < 3.
    """
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    nopunct = regex.sub(" ", text)  # delete stuff but leave at least a space to avoid clumping together
    words = nltk.word_tokenize(nopunct)
    words = [w for w in words if len(w) > 2]  # ignore a, an, to, at, be, ...
    words = [w.lower() for w in words]
    words = [w for w in words if w not in ENGLISH_STOP_WORDS]
    # print words
    return words


def stemwords(words):
    """
    Given a list of tokens/words, return a new list with each word
    stemmed using a PorterStemmer.
    """
    stemmer = PorterStemmer()
    words = [w.decode('ascii', 'ignore') for w in words]
    stemmed = [stemmer.stem(w) for w in words]
    return stemmed

def tokenizer(text):
    return stemwords(tokenize(text))


def compute_tfidf(corpus):
    """
    Create and return a TfidfVectorizer object after training it on
    the list of articles pulled from the corpus dictionary. The
    corpus argument is a dictionary mapping file name to xml text.
    """

    # for file in corpus:
    #     #text = gettext(corpus[file])
    #     #text = tokenizer(text)

    tfidf = TfidfVectorizer(input='content',
                        analyzer='word',
                        preprocessor=gettext,
                        tokenizer=tokenizer,
                        stop_words='english',
                        decode_error = 'ignore')
    text = []
    for file in corpus:
        text.append(corpus[file])
    train_corpus_tf_idf = tfidf.fit_transform(text)
    return tfidf


def summarize(tfidf, text, n):
    """
    Given a trained TfidfVectorizer object and some XML text, return
    up to n (word,score) pairs in a list.
    """
    test_corpus_tf_idf = tfidf.transform([text])
    all_words = tfidf.get_feature_names()
    results = [((i, j), test_corpus_tf_idf[i, j]) for i, j in zip(*test_corpus_tf_idf.nonzero())]
    results = sorted(results, key=lambda tup: tup[1], reverse=True)
    final_list = []
    for i in range(len(results)):
        final_list.append((all_words[results[i][0][1]], results[i][1]))
    final_list = [s for s in final_list if s[1] >= 0.09]
    if len(final_list) < n:
        n = len(final_list)
    return final_list[0:n]



def load_corpus(zipfilename):
    """
    Given a zip file containing root directory reuters-vol1-disk1-subset
    and a bunch of *.xml files, read them from the zip file into
    a dictionary of (word,xmltext) associations. Use namelist() from
    ZipFile object to get list of xml files in that zip file.
    Convert filename reuters-vol1-disk1-subset/foo.xml to foo.xml
    as the keys in the dictionary. The values in the dictionary are the
    raw XML text from the various files.
    """
    zip_ref = zipfile.ZipFile(zipfilename, 'r')
    files = zip_ref.namelist()
    files = files[1:]
    zip_ref.close()
    dict1 = {}
    for file in files:
        file_name = string.split(file, '/')[1]
        dict1[file_name] = open(file, 'r').read()
    return dict1