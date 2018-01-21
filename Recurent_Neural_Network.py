from keras.preprocessing import sequence
from keras.models import Sequential, Model
from keras.layers import Dense, Embedding, Flatten, Dropout, Input, LSTM, Bidirectional, TimeDistributed
from keras.datasets import imdb
from sklearn import metrics
import os
from keras.callbacks import TensorBoard

from gensim.models import KeyedVectors
from Vectorizer import Vectorizer
import Parsers

vocab_size = 20000
maxlen = 100  # cut texts after this number of words (among top max_features most common words)

### other hyperparameters
n_folds = 2
batch_size = 128
nb_epoch = 100
log_path = 'C:\\Users\\Julien\\Desktop\\logs\\TAL\\RNN'
t = TensorBoard(log_dir=log_path, batch_size=batch_size)
emb_file = 'glove.6B.50d.w2v.txt'

print('Loading data...')
# (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=vocab_size)

WtoV = Vectorizer(emb_file)

parser_train = Parsers.VectorParser("eng.train.txt")
documents_train = parser_train.documents
x_train = WtoV.encode_features(documents_train)
y_train = WtoV.encode_annotations(documents_train)

parser_test = Parsers.VectorParser("eng.testa")
documents_test = parser_test.documents
x_test = WtoV.encode_features(documents_test)
y_test = WtoV.encode_annotations(documents_test)

print('Pad sequences (samples x time)')
x_train = sequence.pad_sequences(x_train, maxlen=None, dtype='float32')
x_test = sequence.pad_sequences(x_test, maxlen=None, dtype='float32')

print('x_train shape: {}'.format(x_train.shape))
print('y_train shape: {}'.format(y_train.shape))
print('x_test shape: {}'.format(x_test.shape))
print('y_test shape: {}'.format(y_test.shape))

print('Build MLP model...')
model = Sequential()
model.add(Embedding(vocab_size, 50, input_length=maxlen))
model.add(Flatten())
model.add(Dropout(0.5))
model.add(Dense(units=100, activation='relu',name='dense_layer_in'))
model.add(Dense(units=1, activation='sigmoid',name='dense_layer_out'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

print(model.summary())

print('Train...')
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=nb_epoch,
          validation_data=(x_test, y_test),
          callbacks=[t]
          )

score, acc = model.evaluate(x_test, y_test, batch_size=batch_size)
print('\n')
print('Evaluate score:', score)
print('Evaluate accuracy:', acc)

print('Testing metrics')
y_pred = model.predict_classes(x_test, batch_size=1, verbose=0)
print(metrics.classification_report(y_test, y_pred.flatten()))

model.save_weights(os.path.dirname(os.path.realpath(__file__)) + '\\models\\RNN.e100')