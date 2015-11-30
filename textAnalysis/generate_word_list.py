from pymongo import MongoClient
from article import Article, ArticleDB
from language import LanguageModel, LanguageModel_Mongo
max_articles = 10

#def generate():
client = MongoClient()
db = client['text_illustrator']
articles = db['articles'].find()
#print articles
dutch = LanguageModel("Dutch")
dutch_mongo = LanguageModel_Mongo("", "dutch", None)
parsed = 0
#connect to db
#for each article

articleDB = ArticleDB()
max_articles = 10 #articles.count()
while (parsed < max_articles or max_articles == -1):
    #print "Parsing Article"
    a = articleDB.get(parsed)
    txt = ' '.join(a['text'])
    adate = ' '.join(a['time'])
    url = ''.join(a['url'])
    atitle = ' '.join(a['title'])
    a = Article(text=txt, title=atitle, src=url, date=adate, nid=a['_id'], language_model=dutch)
    a.analyze()
    parsed += 1

#l = dutch.getWordsByFrequency()
print "Inserting into Database"
dutch_mongo.collection.drop()
for k, w in dutch.words.iteritems():
    dutch_mongo.__process_word__(w)

print "Articles Parsed: ", articles.count()
#generate()
