#перед началом подключить библиотеки tensorflow, keras
from tensorflow.python import keras
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense, Embedding, GRU
from keras import utils
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import matplotlib.pyplot as plt

#загрузка данных
max_words = 10000
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_words)

#подготовка данных для обучения
maxlen = 200 #макс длина отзыва
x_train = pad_sequences(x_train, maxlen=maxlen)
x_test = pad_sequences(x_test, maxlen=maxlen)

#создание нейронной сети
model = Sequential()
model.add(Embedding(max_words,8, input_length=maxlen))
model.add(GRU(32, recurrent_dropout = 0.2))
model.add(Dense(1,activation='sigmoid'))

#компилируем
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

#обучаем нейронную сеть
history = model.fit(x_train,
                    y_train,
                    epochs=15,
                    batch_size=128,
                    validation_split=0.1)

plt.plot(history.history['accuracy'],
        label='Доля верных ответов на обучающем наборе')
plt.plot(history.history['val_accuracy'],
        label='Доля верных ответов на проверочном наборе')
plt.xlabel('эпоха обучения')
plt.ylabel('доля верных ответов')
plt.legend()
plt.show()

#проверяем работу сети на тестовом наборе данных
scores = model.evaluate(x_test, y_test, verbose=1)

