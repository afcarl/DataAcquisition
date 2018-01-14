from flask import Flask, render_template
from doc2vec import *
import sys


#glove_filename = '/Users/neerjadoshi/msan/DataAcquisition/data/glove.6B.300d.txt'
#articles_dirname = '/Users/neerjadoshi/msan/DataAcquisition/data/bbc'

app = Flask(__name__)

@app.route("/")
def articles():
    """Show a list of article titles"""

    return render_template('articles.html', articles = articles)


@app.route("/article/<topic>/<filename>")
def article(topic,filename):
    """
    Show an article with relative path filename. Assumes the BBC structure of
    topic/filename.txt so our URLs follow that.
    """
    n = 5
    recommended_docs = recommended(topic+'/'+filename, articles, n)
    article_to_show = topic+'/'+filename
    for sublist in articles:
        if sublist[0] == article_to_show:
            article_to_show = sublist
            break
    return render_template('article.html', recommended_docs = recommended_docs, article = article_to_show)



# initialization
i = sys.argv.index('server:app')
glove_filename = sys.argv[i+1]
articles_dirname = sys.argv[i+2]

gloves = load_glove(glove_filename)
articles = load_articles(articles_dirname, gloves)
