from tfidf import *
import sys
from collections import Counter

xmltext = sys.argv[1]
xmltext = gettext(open(xmltext, 'r').read())
xmltext = tokenizer(xmltext)
ctr = Counter(xmltext).most_common(10)
result_string = ''
for i in range(len(ctr)):
    result_string = result_string + str(ctr[i][0]) + ' ' + str(ctr[i][1]) + '\n'
print result_string.strip()