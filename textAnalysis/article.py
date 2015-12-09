from word import Word
import pymongo

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

    def __update_word__(self, word):
        if word == ' ':
            return
        print word
        if self.words.get(word.lower(), None) == None:
            self.words[word.lower()] = Word(word)

        if self.words[word.lower()].freq == 0:
            self.words[word.lower()].freq += self.words[word.lower()].sub_freq
        self.words[word.lower()].freq += 1
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

    def analyze(self, mxSetSize=1):
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
        #rehersal_loop = []*self.__rehersal_loop_length__
        wset = []
        for w in words:
            """
            get distance from previous words
            """
            if len(wset) >= mxSetSize:
                temp = []
                temp[0:(mxSetSize-1)] = wset[1:mxSetSize]
                wset = temp
            else:
                wset.append(w)

            for j in range(0, len(wset)+1):
                #print wset[0:j]
                #nw = ' '.join(wset[0:j])
                self.__update_word__(' '.join(wset[0:j]))

        if self.language_model != None:
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

    def getSalientSets(self, mxSetSize=1, seperators=[]):
        sets = dict()
        words = words.split(' ')
        setlen = 0
        for wi in range(0, len(words)):
            setlen = max(wi + mxSetSize, len(words))
            wset = []
            for wj in range(wi, setlen):
                "is salient"
                wset.append(words[wi])
                "look up in database"


            print "look up..."

