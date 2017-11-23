import nltk
from nltk.corpus import gutenberg
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

# Run: python -m nltk.downloader gutenberg maxent_treebank_pos_tagger averaged_perceptron_tagger punkt tagsets
moby_dick = gutenberg.raw('melville-moby_dick.txt')
print('Moby Dick sample: {0}'.format(moby_dick[117:300]))

# Séparation des phrases

sentences = [sent for sent in sent_tokenize(moby_dick[117:300])]

# Séparation des mots


# Directement sur le texte
words = word_tokenize(moby_dick[117:300])

# Sur chaque phrase séparément
sentences = [sent for sent in sent_tokenize(moby_dick[117:300])]
sentence_words = [word_tokenize(sentence) for sentence in sentences]

print('-------- Sentences -------')
for (i, sent) in enumerate(sent_tokenize(moby_dick[117:300])):
    print('{}: {}'.format(i, sent))
