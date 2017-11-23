"""
class Parser(object):
    # Classe parente pour tous les parsers

    def create(self):
        return self

    def read_file(self) -> Document:
        filename = "eng.testa"
        with open(filename, 'r', encoding='utf-8') as fp:
            content = fp.read()
        return self.read(content)


class SimpleTextParser(Parser):
    def read(self, content: str) -> Document:
        return Document().create_from_text(content)
"""

from Interval import Interval
from Document import Document
from Token import Token

class VectorParser:
    def __init__(self, file):
        print("init")
        print(file)
        self.documents = []
        self.words = []
        self.sentences = []  # Interval List
        self.labels = []
        self.read(file)

    def read(self, file):
        with open(file, 'r', encoding='utf-8') as fp:
            content = fp.read()
            offset = 0
            current_doc = -1
            for line in content.split('\n'):
                if line.split(' ')[0] == '-DOCSTART-':
                    self.documents.append(
                        {'order': current_doc, 'words': [], 'sentences': [], 'labels': [], 'begin': "", 'end': ""})
                    current_doc += 1
                self.documents[current_doc]['order'] = current_doc
                self.documents[current_doc]['begin'] = offset
                self.documents[current_doc - 1]['end'] = offset - 1
                if not(line.split(' ')[0] in ['', '-DOCSTART-']):
                    self.documents[current_doc]['words'].append(line.split(' ')[0])
                    self.documents[current_doc]['labels'].append(line.split(' ')[-1])
                offset += len(line)

            for document in self.documents:
                begin = 0
                end = 0
                for word in document['words']:
                    if word == '.':
                        document['sentences'].append(Interval(begin, end))
                        begin = end
                    else:
                        end += 1

    def show_doc(self):
        for item in self.documents:
            print('--------------------------------------------------')
            for key in item:
                print(key + ':' + str(item[key]))

if __name__ == '__main__':
    parser = VectorParser("eng.testa")
    parser.show_doc()

    doc = Document()
    doc.create_from_vectors(parser.documents[0]['words'],
                            parser.documents[0]['sentences'],
                            parser.documents[0]['labels'])
