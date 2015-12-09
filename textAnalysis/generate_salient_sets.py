def salient_sets(article_set, model):
    print "Generating Salience Sets..."

    print "Finished Generating Salience Sets..."
    return []


lang = LanguageModel_Mongo("", "dutch", None)
articles = ArticleDB()

a = articles.get(0)
s = a.getSalientSets()

#for each article
#get words
#remove words frequent across articles
