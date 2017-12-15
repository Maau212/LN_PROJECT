from keras.preprocessing import sequence
from keras.models import Sequential, Model
from keras.layers import Dense, Embedding, Flatten, Dropout, Input, LSTM, Bidirectional, TimeDistributed
from keras.datasets import imdb
from sklearn import metrics

vocab_size = 20000
maxlen = 100  # cut texts after this number of words (among top max_features most common words)
batch_size = 32

print('Loading data...')
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=vocab_size)

print('Pad sequences (samples x time)')
x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
x_test = sequence.pad_sequences(x_test, maxlen=maxlen)

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
          epochs=10,
          validation_data=(x_test, y_test))

score, acc = model.evaluate(x_test, y_test, batch_size=batch_size)
print('\n')
print('Evaluate score:', score)
print('Evaluate accuracy:', acc)

print('Testing metrics')
y_pred = model.predict_classes(x_test, batch_size=1, verbose=0)
print(metrics.classification_report(y_test, y_pred.flatten()))