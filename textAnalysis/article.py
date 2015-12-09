from word import Word
import pymongo
from language import LanguageModel_Mongo, LanguageInfoModel_Mongo

class ArticleDB(object):
    __client = pymongo.MongoClient()
    __database = __client['text_illustrator']
    __collection = __database['articles']

    def update(self, article):
        "update article"

    def get(self, index=-1, ref=""):
        if isinstance(index, list):
            return None
        elif index >= 0:
            return self.__collection.find()[index]
        elif index == -1:
            return self.__collection.find(ref)

    def count(self):
        return self.__collection.count()
    """
    def get(self, ref):
        if isinstance(ref, list):
            "get each reference"
        else:
            "get article"
            return None
    """
class ArticleRef(object):
    def __init__(self, url=None, title=None, _id=None):
        self.url = url
        self.title = title
        self._id = _id

    def load(self):
        db = ArticleDB()
        return db.get(ref={"_id":self._id})
"""
1) Get Word Frequency per [article, language, site]
2) Get Word Pair Frequency/Co-relation
3) Sub-Words
"""
class Article(object):
    #__words__ = dict()
    sentences = []
    rehersal_loop_length = 7
    #__rehersal_loop__ = []
    enable_subwords = False
    enable_punctiation = True #this technically is not apriori
    enable_sentences = False #this technically is not apriori
    min_subword_size = 1

    def __init__(self, text=None, src=None, title=None, date=None, language_model=None, nid=None):
        self.text = text
        self.src = src
        self.words = dict()
        self.rehersal_loop = []
        self.language_model = language_model
        self._id = nid
        self.date = date
        self.title = title

    def getRef(self):
        return {"src":self.src, "title":self.title, "_id":self._id}

    def __update_subword__(self, subword, word):
        if self.words.get(subword.lower(), None) == None:
            self.words[subword.lower()] = Word(subword.lower())

        w = self.words[subword.lower()]
        w.subword_frequency += 1
        if w.word_frequency > 0:
            w.word_frequency += 1

        w.superwords[word.lower()] = w.superwords.get(word.lower(), 0) + 1

    def __update_word__(self, word, word_count):
        if word == ' ':
            return
        #print word
        if self.words.get(word.lower(), None) == None:
            self.words[word.lower()] = Word(word)

        if self.words[word.lower()].freq == 0:
            self.words[word.lower()].freq += self.words[word.lower()].sub_freq
        self.words[word.lower()].freq += 1
        self.words[word.lower()].word_count = word_count
        """
        update frequency
        """
        if self.enable_subwords:
            for sub_word_length in range(self.min_subword_size, len(word)):
                for pad in range(0, len(word)-sub_word_length):
                    start_sword = pad
                    end_sword = pad + sub_word_length
                    sub_word = word[start_sword:end_sword]

                    self.__update_subword__(sub_word, word)

    def analyze(self, mxSetSize=1, update_model=True):
        for w in self.genWordSets(mxSetSize):
            self.__update_word__(w[0], w[1])

        if self.language_model != None and update_model:
            for k, v in self.words.iteritems():
                #v.addArticle(self)
                self.language_model.update_word(v, self)

    def getWordsByFrequency(self):
        wordsByFreq = dict()
        mxFreq = 0
        for k, v in self.words.iteritems():
            freq = v.freq
            bucket = wordsByFreq.get(freq, [])
            if bucket == []:
                wordsByFreq[freq] = bucket
            if mxFreq < freq:
                mxFreq = freq

            bucket.append([k,v])

        return wordsByFreq

    def genWordSets(self, mxSize):
        words = self.text.replace('\n',' ')
        words = words.replace('\t',' ')
        words = words.replace('.', '')
        words = words.replace(',', '')
        words = words.replace('/', '')
        words = words.replace('(', '')
        words = words.replace(')', '')
        words = words.replace(';', '')
        words = words.replace('\"', '')
        words = words.replace('\'', '')
        words = words.replace('?', '')
        words = words.replace('!', '')
        words = words.replace('[', '')
        words = words.replace(']', '')
        words = words.split(' ')

        wset = []
        for w in words:
            if len(wset) >= mxSize:
                temp = wset[1:mxSize]
                wset = temp
            elif w != '' and w != ' ':
                wset.append(w)

                for i in range(1, len(wset)+1):
                    yield [' '.join(wset[0:i]), i]

    def getSalientSets(self, lang, mxSetSize=1, AFreqP=0.20, OFreqP=0.0625):
        sets = dict()
        words = self.text.replace('\n',' ')
        words = words.replace('\t',' ')
        words = words.replace('.', '')
        words = words.replace(',', '')
        words = words.replace('/', '')
        words = words.replace('(', '')
        words = words.replace(')', '')
        words = words.replace(';', '')
        words = words.replace('\"', '')
        words = words.replace('?', '')
        words = words.replace('!', '')
        words = words.replace('[', '')
        words = words.replace(']', '')
        words = words.split(' ')
        setlen = 0
        l = LanguageInfoModel_Mongo()
        linfo = l.getLanguage(self.language_model.lang)

        AFreq = linfo["articleCount"]*AFreqP
        OFreq = linfo["maxFreq"]*OFreqP

        ret = []
        for w in self.genWordSets(mxSetSize):
            wdata = self.language_model.getWord(w[0])
            if wdata != None:
                #print "TEST ", w
                wAFreq = wdata.articleCount()
                #print wdata.articles
                wOFreq = wdata.getFreq()
                articleSaliencyScore = 1 - float(self.words[w[0]].freq)/float(len(self.words.keys()))
                if wOFreq < OFreq and wAFreq < AFreq:
                    ret.append([w[0], articleSaliencyScore])

        return ret
