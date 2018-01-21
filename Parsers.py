from Interval import Interval
from Document import Document
from Token import Token
from Token import Sentence

class VectorParser:
    def __init__(self, file):
        self.documents = []
        self.words = []
        self.features = []
        self.sentences = []  # Interval List
        self.labels = []
        self.read(file)

    def read(self, file):
        with open(file, 'r') as fp:
            content = fp.read()
            docs = content.split("-DOCSTART- -X- O O")
            for doc in docs:
                word_list = []
                label_list = []
                sentences_list = []
                offset = 0
                if doc == '':
                    continue
                for sentence in doc.strip().split("\n\n"):
                    start = offset
                    if sentence == '':
                        continue
                    for line in sentence.split("\n"):
                        words = line.split(" ")
                        offset += 1
                        word_list.append(words[0].strip())
                        label_list.append(words[-1])
                    sentences_list.append(Interval(start, offset))
                    offset += 1
                self.documents.append(Document().create_from_vectors(word_list, sentences_list, label_list))

    def read_old(self, file):
        """
        Read a document and parse it in words, sentences and labels
        :param name of the file to parse
        :return: A list of triplets (words,sentences,labels), one for each document parsed.
        """

        with open(file, 'r') as fp:
            content = fp.read()
            offset = 0
            current_doc = -1
            for line in content.split('\n'):
                if line.split(' ')[0] == '-DOCSTART-':
                    self.features.append(
                        {'order': current_doc, 'words': [], 'sentences': [], 'labels': [], 'begin': "", 'end': ""})
                    current_doc += 1
                self.features[current_doc]['order'] = current_doc
                self.features[current_doc]['begin'] = offset
                self.features[current_doc - 1]['end'] = offset - 1
                if not(line.split(' ')[0] in ['', '-DOCSTART-']):
                    self.features[current_doc]['words'].append(line.split(' ')[0])
                    self.features[current_doc]['labels'].append(line.split(' ')[-1])
                offset += len(line)

            for document in self.features:
                begin = 0
                end = 0
                for word in document['words']:
                    if word == '.':
                        document['sentences'].append(Interval(begin, end))
                        begin = end
                    else:
                        end += 1

        for feature in self.features:
            self.documents.append(Document.create_from_vectors(
                self.features[self.features.index(feature)]['words'],
                self.features[self.features.index(feature)]['sentences'],
                self.features[self.features.index(feature)]['labels']))

    def show_doc_old(self):
        for item in self.documents:
            for key in item:
                print(key + ':' + str(item[key]))

    def show_doc(self):
        for item in self.documents:
            print('--------------------------------------------------------------------------')
            print(item.show())

if __name__ == '__main__':
    parser = VectorParser("eng.testa")
    # parser = VectorParser("frWiki_no_phrase_no_postag_1000_skip_cut100.bin")

    parser.show_doc()