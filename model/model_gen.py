import pandas as pd
import matplotlib.pyplot as plt
import re
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, Dense, LSTM
from tensorflow.keras.models import Sequential

print('Load data..')
train_data= pd.read_table("data/ratings_train.txt")
test_data= pd.read_table("data/ratings_test.txt")

# Null값 지우기
print('Deleting null..')
train_data=train_data.dropna(how='any') 

# 특수문자 제거
print('Delete special character..')
train_data['document'] = train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")

# 토큰화, 불용어 제거
stopwords=['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다'] 
okt = Okt()
print('tockenization and delete stopwords..(train data)')
X_train=[]
for sentence in train_data['document']:
    temp_X = []
    temp_X=okt.morphs(sentence, stem=True)
    temp_X=[word for word in temp_X if not word in stopwords]
    X_train.append(temp_X)

print('tockenization and delete stopwords..(test data)')
X_test=[]
for sentence in test_data['document']:
    temp_X = []
    temp_X=okt.morphs(sentence, stem=True)
    temp_X=[word for word in temp_X if not word in stopwords]
    X_test.append(temp_X)   


# 정수 인코딩
print('Indexing..')
max_words = 35000
tokenizer = Tokenizer(num_words=max_words) # 상위 35,000개의 단어만 보존
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)

# 입력 길이 맞추기
print('Size synch..')
max_len=30
X_train = pad_sequences(X_train, maxlen=max_len)
X_test = pad_sequences(X_test, maxlen=max_len)

# 출력값 별도 array에 저장
print('Set output array..')
y_train=np.array(train_data['label'])
y_test=np.array(test_data['label'])
print(y_train,y_test)

# 모델 학습하기
print('Configure model..')
model = Sequential()
model.add(Embedding(max_words, 100))
model.add(LSTM(128))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
print('Learning model..')
history = model.fit(X_train, y_train, epochs=4, batch_size=60, validation_split=0.2)

print("\n Accuracy: %.4f" % (model.evaluate(X_test, y_test)[1]))

print(model.summary())
print('Save model..')
model.save('movie_review_model.h5')