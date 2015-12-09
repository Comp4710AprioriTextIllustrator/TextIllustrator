from pymongo import MongoClient
from article import Article, ArticleDB
from language import LanguageModel, LanguageModel_Mongo
max_articles = 10
mxSetSize = 1
lang = "English"
#def generate():

sites = ["bbc.com", "bbc.co.uk"]
def generate_model(lang, sites, settings, mxParse=100):
    model = LanguageModel(lang)
    mongo = LanguageModel_Mongo("", lang, None)
    parsed = 0

    articleDB = ArticleDB()
    while (parsed < mxParse or (max_articles == -1 and articleDB.count())):
        a = articleDB.get(index=parsed)
        txt = ' '.join(a.get('text',''))
        adate = ' '.join(a.get('time',''))
        url = ''.join(a.get('url',''))
        atitle = ' '.join(a.get('title',''))
        for s in sites:
            if s in url:
                a = Article(text=txt, title=atitle, src=url, date=adate, nid=a['_id'], language_model=model)

        a.analyze(mxSetSize)
        parsed += 1

    print "Parsed ", parsed, " Articles. Inserting into Database"
    mongo.collection.drop()
    for k, w in model.words.iteritems():
        mongo.__process_word__(w)

generate_model(lang, sites, None, 100)
