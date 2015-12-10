from pymongo import MongoClient
from article import Article, ArticleDB
from language import LanguageModel, LanguageModel_Mongo

def get_article(article):
    txt = ' '.join(article.get('text',''))
    adate = ' '.join(article.get('time',''))
    url = ''.join(article.get('url',''))
    atitle = ""
    if isinstance(article.get('title', []), list):
        atitle = ' '.join(article.get('title',''))
    elif isinstance(article.get('title', ""), basestring):
        atitle = article.get('title', "")

    return Article(text=txt, title=atitle, src=url, date=adate, nid=article['_id'], language_model=model)

def salient_sets(article_set, model, mxSetSize=2, AFreqP=0.05, OFreqP=0.03125):
    print "Generating Salience Sets..."
    ret = []
    for aj in article_set:
        article = get_article(aj)
        article.analyze(mxSetSize, update_model=False)
        #ret.append(article)
        ret.append(article.getSalientSets(model.lang, mxSetSize, AFreqP, OFreqP))
    print "Finished Generating Salience Sets..."
    return ret



#Example
"""
model = LanguageModel_Mongo("", "English", None)
articles = ArticleDB()

a = [articles.get(0), articles.get(1)]
ret = salient_sets(a, model)
"""

