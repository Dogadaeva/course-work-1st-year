from tensorflow.python import keras #установить tensorflow и keras
from keras.models import Sequential
from keras.layers import Dense, Embedding, MaxPooling1D, Conv1D, GlobalMaxPooling1D, Dropout
from keras import utils
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.callbacks import ModelCheckpoint
import pandas as pd #установить pandas
import numpy as np
import matplotlib.pyplot as plt
import wget #установить wget

num_words = 10000
max_review_len = 100
#Загрузка набора данных
#функция wget

#Просматриваем данные
#функция head

#Загружаем данные в память
train = pd.read_csv('yelp_review_polarity_csv/train.csv',
                    header=None,
                    names=['Class', 'Review'])
#Выделяем данные для обучения
reviews = train['Review']
#Выделяем правильные ответы
y_train = train['Class'] - 1
#Токенизация текста
tokenizer = Tokenizer(num_words=num_words)
tokenizer.fit_on_texts(reviews) #обучаем
#Просматриваем словарь токенизатора
print(tokenizer.word_index)
#Преобразуем отзывы Yelp в числовое представление
sequences = tokenizer.texts_to_sequences(reviews)
#Просматриваем отзывы в числовом представлении
index = 100
print(reviews[index])
print(sequences[index])
#Ограничиваем длину отзывов
x_train = pad_sequences(sequences, maxlen=max_review_len)


#Создаем нейронную сеть
model = Sequential()
model.add(Embedding(num_words, 64, input_length=max_review_len))
model.add(Conv1D(250, 5, padding='valid', activation='relu'))
model.add(GlobalMaxPooling1D())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.summary()

#Обучаем нейронную сеть
history = model.fit(x_train,
                    y_train,
                    epochs=4,
                    batch_size=128,
                    validation_split=0.1)
plt.plot(history.history['accuracy'],
         label='Доля верных ответов на обучающем наборе')
plt.plot(history.history['val_accuracy'],
         label='Доля верных ответов на проверочном наборе')
plt.xlabel('Эпоха обучения')
plt.ylabel('Доля верных ответов')
plt.legend()
plt.show()


#Загружаем набор данных для тестирования
test = pd.read_csv('yelp_review_polarity_csv/test.csv',
                    header=None,
                    names=['Class', 'Review'])
test_sequences = tokenizer.texts_to_sequences(test['Review'])
x_test = pad_sequences(test_sequences, maxlen=max_review_len)
#Правильные ответы
y_test = test['Class'] - 1

#Оцениваем качество работы сети на тестовом наборе данных
model.evaluate(x_test, y_test, verbose=1)


#Оцениваем тональность на собственном отзыве
text = '''The SmartBurger restaurant is awful. It’s a small shabby place.
The food is really bad and very expensive.  The host and waiters are rud.
I will never visit the SmartBurger again!
'''
sequence = tokenizer.texts_to_sequences([text])
data = pad_sequences(sequence, maxlen=max_review_len)
result = model.predict(data)
if result < 0.5:
    print('Отзыв отрицательный')
else:
    print('Отзыв положительный')