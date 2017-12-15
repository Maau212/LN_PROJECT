from unittest import TestCase
from Document import Document
from Interval import Interval
from Parsers import VectorParser
class TestDocument(TestCase):
    def test_create_from_text(self):
        doc = Document()
        text =""
        self.assertRaises(Exception,doc.create_from_text(), text)
        self.fail()

    def test_create_from_vectors(self):
        doc = Document()

        text = "Il était une fois." \
               "Ils vécurent heureux et eurent beaucoup de chocobons."

        words = ["Il","était","une","fois",".","Ils","vécurent","heureux","et","eurent","beaucoup","de","chocobons"]

        sentences = [Interval(0,
                              len("Il était une fois.")),
                     Interval(len("Il était une fois."),
                              len("Ils vécurent heureux et eurent beaucoup de chocobons."))]

        labels = []

        #create Document() from first doc parsed vectors
        doc.create_from_vectors(words, sentences, labels)

        tokens = []
        self.assertEqual(doc.tokens, tokens, "Tokens failed")

    def test_get_shape_category(self):
        self.fail()

    def test__retokenize(self):
        self.fail()

    def test__find_tokens(self):
        self.fail()

    def test__find_sentences(self):
        self.fail()
