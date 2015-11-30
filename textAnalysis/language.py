import logging
import pymongo
from word import Word
logger = logging.getLogger(__name__)

class LanguageModel(object):
    def __init__(self, language):
        self.words = dict()
        self.language = language
    def update_word(self, word, article):
        "update word"
        b = self.words.get(word.key(), None)
        if b == None:
            self.words[word.key()] = word
            self.words[word.key()].addArticle(article)
        else:
            b.addArticle(article)
            b.freq += word.freq
            b.sub_freq += word.sub_freq
            for k, v in word.superwords.iteritems():
                bucket = b.superwords.get(k, None)
                if bucket == None:
                    b.superwords[k] = v
                else:
                    b.superwords[k] += v

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

            bucket.append([k, v])

        return wordsByFreq
        """
        flatList = []
        for i in reversed(range(1, mxFreq)):
            flatList = flatList + wordsByFreq.get(i, [])

        return flatList
        """

class LanguageModel_Mongo(object):
    def __init__(self, lang_uri, lang_db, languageModel):
        self.lang_uri = lang_uri
        self.lang_db = lang_db
        self.client = pymongo.MongoClient()
        self.db = self.client["text_illustrator"]
        self.collection = self.db[self.lang_db]

    def __load_from_langmodel__(self, languageModel):
        print "Loading language Model"

    def update_word(self, word, article):
        b = self.getWord(word.key())

        if b == None:
            word.addArticle(article)
            self.__process_word__(word)
        else:
            b.addArticle(article)
            b.freq += word.freq
            b.sub_freq += word.sub_freq
            for k, v in word.superwords.iteritems():
                bucket = b.superwords.get(k, None)
                if bucket == None:
                    b.superwords[k] = v
                else:
                    b.superwords[k] += v
            self.__update_word__(b)

    def __update_word__(self, word):
        "update word"
        wentry = {"word":word.key(), "freq":word.getFreq(), "sub_freq":word.getSubFreq(), "superwords":word.getSuperWords(), "articles":word.getArticlesByRef()}
        self.collection.update_one({"_id":word._id}, {"$set":wentry})
    def __process_word__(self, word):
        "process word"
        wentry = {"word":word.key(), "freq":word.getFreq(), "sub_freq":word.getSubFreq(), "superwords":word.getSuperWords(), "articles":word.getArticlesByRef()}
        self.collection.insert_one(wentry)

    def getWord(self, word):
        if isinstance(word, basestring):
            w = self.collection.find_one({"word":word})
            if w == None:
                return w
            wn = Word(word)
            wn.__dict__ = w
            return wn
        else:
            print "Error Querying Database with ", word
            return None
