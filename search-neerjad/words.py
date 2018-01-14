import os
import re
import string
from jinja2 import Template
import codecs

def filelist(root):
    """Return a fully-qualified list of filenames under root directory"""

    os.chdir(root)

    files = []
    for fname in os.listdir(os.getcwd()):
        if os.path.isdir(os.path.join(os.getcwd(), fname)):
            file_path = os.path.join(os.getcwd(), fname)
            for file in os.listdir(file_path):
                files.append(os.path.join(file_path, file))

        else:
            files = [os.path.join(root,file) for file in  os.listdir(root)]
    return files

def get_text(fileName):
    #f = open(fileName)
    f = codecs.open(fileName, encoding='utf-8', mode='r')
    s = f.read()
    f.close()
    return s


def words(text):
    """
    Given a string, return a list of words normalized as follows.
    Split the string to make words first by using regex compile() function
    and string.punctuation + '0-9\\r\\t\\n]' to replace all those
    char with a space character.
    Split on space to get word list.
    Ignore words < 3 char long.
    Lowercase all words
    """
    # FIx!!
    '''
    regex = re.compile('[%s]' % (re.escape(string.punctuation +'\r\t\n]') + '0-9'))
    text = regex.sub(' ', text)
    text = text.split(' ')
    new_text = []
    for word in text:
        if len(word) >= 3:
            new_text.append(string.lower(word))
    return new_text
    '''
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    nopunct = regex.sub(" ", text)  # delete stuff but leave at least a space to avoid clumping together
    words = nopunct.split(" ")
    words = [w for w in words if len(w) > 2]  # ignore a, an, to, at, be, ...
    words = [w.lower() for w in words]
    # print words
    return words

def results(docs, terms):
    """
    Given a list of fully-qualifed filenames, return an HTML file
    that displays the results and up to 2 lines from the file
    that have at least one of the search terms.
    Return at most 100 results.  Arg terms is a list of string terms.
    """
    headers = []
    data = []
    start = None
    end = None
    search_string = ''
    for item in terms:
        search_string = search_string + item + ' '
    search_string.strip()
    if docs == None:
        return 'Not found'
    org_docs = len(docs)
    if len(docs) >= 100:
        docs = docs[0:99]

    for i in range(0, len(docs)):
        headers.append(docs[i])
        data_temp = open(docs[i], 'r')
        data_temp = data_temp.readlines()
        count = 0
        data1 = ''
        for line in data_temp:
            if any(term in line.lower() for term in terms):
                data1 = data1 + line + '<br>'
                count = count + 1
            if count == 2:
                break
        data.append(data1)

    extention = 'file:///'
    # creating html template
    html_template = '''
    <html>
    <body>
    <h2>Search results for <b>{{search_string}}</b> in {{org_docs}} files</h2>
    {% for i in range(0,header_count)%}
    <p><a href={{extention + headers[i]}}>{{headers[i]}}</a><br>
    {{data[i]}}<br>
    {% endfor %}
    </body>
    </html>
    '''

    # rendering html
    html_out = Template(html_template).render \
        (headers=headers, data=data, header_count = len(headers), extention = extention, search_string = search_string, org_docs = org_docs)

    return html_out


def filenames(docs):
    """Return just the filenames from list of fully-qualified filenames"""
    if docs is None:
        return []
    return [os.path.basename(d) for d in docs]
