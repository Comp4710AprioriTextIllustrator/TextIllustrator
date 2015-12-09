import unittest
from article import Article

sentenceA = "A quick brown fox jumps over the lazy dog"
sentenceB = "Right righting"
sentenceC = "a A a b B b c C C d D d d"
sentenceD = "a aR"
sentenceE = "b bR a aR abR ababR"
class TestTextAnalysis(unittest.TestCase):
    """
    def test_sentence(self):
        a = Article(text=sentenceA)
        a.analyze()

        for k, v in a.__words__.iteritems():
            self.assertTrue(v.__word_frequency__ <= 1)
            self.assertTrue(v.__subword_frequency__ <= 4)
            self.assertTrue(len(v.__superwords__.values()) <= 4)

    def test_sentence2(self):
        print "SENTENCE 2"
        a = Article(text=sentenceB)
        a.analyze()

        print a.__text__
        print a.__words__
        for k, v, in a.__words__.iteritems():
            print k
            print "value ", v.__subword_frequency__
            print "value2 ", v.__superwords__
            self.assertTrue(v.__word_frequency__ <= 1)
            self.assertTrue(v.__subword_frequency__ <= 3)
            self.assertTrue(len(v.__superwords__.values()) <= 3)
    """
    """
    def test_sentenceDiag(self):
        a = Article(text=sentenceE)
        a.analyze()

        for k, v in a.__words__.iteritems():
            print k
            print v.__subword_frequency__
            print v.__superwords__
            print v.__word_frequency__
    """
    def test_sentence3(self):
        a = Article(text=sentenceC)
        a.analyze()

        mFreq = 0
        for k, v in a.__words__.iteritems():
            self.assertTrue(v.__subword_frequency__ == 0)
            self.assertTrue(len(v.__superwords__) == 0)
            if mFreq < v.__word_frequency__:
                mFreq = v.__word_frequency__
            self.assertTrue(v.__word_frequency__ <= 4)

        self.assertTrue(mFreq == 4)

    def test_sentence4(self):
        a = Article(text=sentenceD)
        a.analyze()

        mFreq = 0
        for k, v in a.__words__.iteritems():
            self.assertTrue(v.__subword_frequency__ <= 1)
            self.assertTrue(len(v.__superwords__) <= 1)
            if mFreq < v.__word_frequency__:
                mFreq = v.__word_frequency__
            self.assertTrue(v.__word_frequency__ <= 2)

        self.assertTrue(mFreq == 2)

    def test_sentence5(self):
        a = Article(text=sentenceE)
        a.analyze()

        mFreq = 0
        for k, v in a.__words__.iteritems():
            self.assertTrue(v.__subword_frequency__ <= 4)
            self.assertTrue(len(v.__superwords__) <= 3)
            if mFreq < v.__word_frequency__:
                mFreq = v.__word_frequency__
            self.assertTrue(v.__word_frequency__ <= 5)

        print mFreq
        self.assertTrue(mFreq == 5)
