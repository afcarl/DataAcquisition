from tfidf import *

zipfilename = sys.argv[1]
summarizefile = sys.argv[2]

corpus = load_corpus(zipfilename)
tfidf = compute_tfidf(corpus)
scores = summarize(tfidf, corpus[summarizefile], 20)
#scores = [s for s in scores if s[1] >= 0.09]
result_string = ''
for i in range(len(scores)):
    result_string = result_string + scores[i][0] + ' ' + '{0:.3f}'.format(scores[i][1]) + '\n'
print result_string.strip()