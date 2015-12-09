from pymongo import MongoClient
from article import Article, ArticleDB
from language import LanguageModel, LanguageModel_Mongo

mxSetSize=1
lang = "English"
def get_article(article):
    txt = ' '.join(a.get('text',''))
    adate = ' '.join(a.get('time',''))
    url = ''.join(a.get('url',''))
    atitle = ""
    if isinstance(a.get('title', []), list):
        atitle = ' '.join(a.get('title',''))
    elif isinstance(a.get('title', ""), basestring):
        atitle = a.get('title', "")

    return Article(text=txt, title=atitle, src=url, date=adate, nid=a['_id'], language_model=model)

def salient_sets(article_set, model):
    print "Generating Salience Sets..."
    ret = []
    for a in article_set:
        article = get_article(a)
        article.analyze(mxSetSize, update_model=False)
        ret.append(article.getSalientSets(model.lang))
    print "Finished Generating Salience Sets..."
    return ret


model = LanguageModel_Mongo("", lang, None)
articles = ArticleDB()

a = articles.get(0)

ret = salient_sets([a], model)

#for each article
#get words
#remove words frequent across articles
