from pymongo import MongoClient
from article import Article, ArticleDB
from language import LanguageModel, LanguageModel_Mongo, LanguageInfoModel_Mongo
#def generate():

#sites = ["bbc.com", "bbc.co.uk"]
def generate_model(lang, sites, mxParse=-1, mxSetSize=3):
    model = LanguageModel(lang)
    mongo = LanguageModel_Mongo("", lang, None)
    parsed = 0

    articleDB = ArticleDB()
    while (parsed < mxParse or (mxParse == -1 and parsed < articleDB.count())):
        a = articleDB.get(index=parsed)
        txt = ""#' '.join(a.get('text',''))
        adate = ' '.join(a.get('time',''))
        url = ""#''.join(a.get('url',''))
        atitle = ""

        if isinstance(a.get('url', []), list):
            url = ' '.join(a.get('url',''))
        elif isinstance(a.get('url', ""), basestring):
            url = a.get('url', "")
        if isinstance(a.get('text', []), list):
            txt = ' '.join(a.get('text',''))
        elif isinstance(a.get('text', ""), basestring):
            txt = a.get('text', "")
        if isinstance(a.get('title', []), list):
            atitle = ' '.join(a.get('title',''))
        elif isinstance(a.get('title', ""), basestring):
            atitle = a.get('title', "")
        for s in sites:
            if s in url:
                a = Article(text=txt, title=atitle, src=url, date=adate, nid=a['_id'], language_model=model)
                a.analyze(mxSetSize)


        parsed += 1

    print "Parsed ", parsed, " Articles. Inserting into Database"
    mongo.collection.drop()
    for k, w in model.words.iteritems():
        mongo.__process_word__(w)

    #Update Language Info
    langInfo = LanguageInfoModel_Mongo()

    keys = sorted(model.words.keys())
    freq = model.getWordsByFrequency()

    langInfo.updateLanguage(lang, parsed, len(model.words.keys()), sorted(freq.keys())[len(freq)-1], sites)

    return mongo

"""
Example
"""
#m = generate_model("English", ["bbc.com", "bbc.co.uk"], -1, 1)
