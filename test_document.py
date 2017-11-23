from unittest import TestCase
from Document import Document

class TestDocument(TestCase):
    def test_create_from_text(self):
        doc = Document()
        self.assertRaises(Exception,doc.create_from_text(), text)
        self.fail()

    def test_create_from_vectors(self):
        self.fail()

    def test_get_shape_category(self):
        self.fail()

    def test__retokenize(self):
        self.fail()

    def test__find_tokens(self):
        self.fail()

    def test__find_sentences(self):
        self.fail()
