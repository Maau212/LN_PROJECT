from gensim.models import KeyedVectors
from typing import List
from Document import Document
import numpy as np
import Parsers


class Vectorizer:
    """ Transform a string into a vector representation"""

    def __init__(self, word_embedding_path: str):
        """
        :param word_embedding_path: path to gensim embedding file
        """
        # Load word embeddings from file
        # self.word_embeddings = KeyedVectors.load_word2vec_format("D:/Project/nlp/NLP_ESGI/External/glove.6B.50d.w2v.txt")
        self.word_embeddings = KeyedVectors.load_word2vec_format(word_embedding_path, binary=False)

        # Create POS to index dictionary
        self.pos2index = {'$': 0, '\'\'': 1, '(': 2, ')': 3, ',': 4, '--': 5, '.': 6, ':': 7, 'CC': 8, 'CD': 9,
                          'DT': 10, 'EX': 11, 'FW': 12, 'IN': 13, 'JJ': 14, 'JJR': 15,
                          'JJS': 16, 'LS': 17, 'MD': 18, 'NN': 19, 'NNP': 20, 'NNPS': 21,
                          'NNS': 22, 'PDT': 23, 'POS': 24, 'PRP': 25, 'PRP$': 26, 'RB': 27, 'RBR': 28, 'RBS': 29,
                          'RP': 30, 'SYM': 31, 'TO': 32, 'UH': 33, 'VB': 34, 'VBD': 35,
                          'VBG': 36, 'VBN': 37, 'VBP': 38, 'VBZ': 39, 'WDT': 40, 'WP': 41, 'WP$': 42, 'WRB': 43,
                          '``': 44}

        # Create shape to index dictionary
        self.shape2index = {'NL': 0, 'NUMBER': 1, 'SPECIAL': 2, 'ALL-CAPS': 3, '1ST-CAP': 4, 'LOWER': 5, 'MISC': 6}

        # Create labels to index
        self.labels = ['O', 'PER', 'LOC', 'ORG', 'MISC']

        self.labels2index = {'O': 0, 'PER': 1, 'I-PER': 1, 'B-PER': 1, 'LOC': 2, 'I-LOC': 2, 'B-LOc': 2, 'ORG': 3,
                             'I-ORG': 3, 'B-ORG': 3, 'MISC': 4, 'I-MISC': 4, 'B-MISC': 4}

    def encode_features(self, documents: List[Document]):
        """
        Creates a feature matrix for all documents in the sample list
        :param documents: list of all samples as document objects
        :return: lists of numpy arrays for word, pos and shape features.
                 Each item in the list is a sentence, i.e. a list of indices (one per token)
        """
        # Loop over documents
        #    Loop over sentences
        #        Loop over tokens
        #           Convert features to indices
        #           Append to sentence
        #   append to sentences
        # return word, pos, shape

        encoded_features = []
        for doc in documents:
            for sentences in doc.sentences:
                sentence = []
                for token in sentences.tokens:
                    sentence.append(self.word_embeddings[token._text.lower()] if token._text.lower() in self.word_embeddings else self.word_embeddings['date'])
                    sentence.append(self.pos2index[token._pos])
                    sentence.append(self.shape2index[token._shape])
                encoded_features.append(np.array(sentence))
        return encoded_features

    def encode_annotations(self, documents: List[Document]):
        """
        Creates the Y matrix representing the annotations (or true positives) of a list of documents
        :param documents: list of documents to be converted in annotations vector
        :return: numpy array. Each item in the list is a sentence, i.e. a list of labels (one per token)
        """
        # Loop over documents
        #    Loop over sentences
        #        Loop over tokens
        #           Convert label to numerical representation
        #           Append to sentence
        # return labels
        sentences_label = []
        for doc in documents:
            for sentences in doc.sentences:
                labels = []
                for token in sentences.tokens:
                    if token._label in self.labels:
                        labels.append(self.labels2index[token._label])
                    else:
                        labels.append(5)
                sentences_label.append(labels)
        return np.array(sentences_label)

if __name__ == '__main__':
    parser = Parsers.VectorParser("eng.testa")
    print(Vectorizer('glove.6B.50d.w2v.txt').encode_features(parser.documents))
