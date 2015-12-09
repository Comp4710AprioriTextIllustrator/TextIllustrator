#import article

class Word:
    def __init__(self, word, word_count=1, sub_freq=0, freq=0,superwords=dict()):
        self.word = word.lower()#spelling
        self.word_count = word_count #for pairs
        self.sub_freq = sub_freq #only relevant if it is an actual word
        self.freq = freq
        self.articles = [] #articles that use this word
        self.superwords = superwords #possible words that contain this one

    def addArticle(self, article):
        #if isinstance(article, article.Article):
        if article in self.articles:
            print "Already Exists"
        else:
            self.articles.append(article)

    def key(self):
        return self.word

    def getFreq(self):
        return self.freq

    def getSubFreq(self):
        return self.sub_freq

    def articleCount(self):
        return len(self.articles)
    def getArticlesByRef(self):
        if isinstance(self.articles, dict):
            return self.articles

        refs = []
        for article in self.articles:
            if isinstance(article, dict):
                refs.append(article)
            else:
                refs.append(article.getRef())

        return refs

    def getSuperWords(self):
        return self.superwords
