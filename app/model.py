#-*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow import keras
from tensorflow.keras.layers import Embedding, Dense, LSTM
from tensorflow.keras.models import Sequential
import re
import json


class MyModel:
    loaded_model=Sequential()

    def __init__(self, loaded_model):
        self.loaded_model=keras.models.load_model('./model/model_file.h5')

    def textPreproc(self, text_in):
        ''' Delete Special Character '''
        temp_text=re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z]","", text_in)
    
        ''' Tockenization and Delete Stopword '''
        okt = Okt()
        okt.morphs
        tocken_text=[]
        tocken_text=okt.morphs(temp_text, stem=True) 
    
        ''' Delete Stopword '''
        stopwords=['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다'] # Stopword List
        tocken_text=[word for word in tocken_text if not word in stopwords] 
        tocken_text = [tocken_text]

        ''' Indexing '''
        with open('./model/tokenizer.json') as f:
            data = json.load(f)
            tokenizer = tokenizer_from_json(data)
        tocken_text = tokenizer.texts_to_sequences(tocken_text)
        
        ''' Array Size Synch '''
        max_array_len=30
        preprocessed_data = pad_sequences(tocken_text, maxlen=max_array_len)
        
        return preprocessed_data
    
    def predict(self, text):
        predict_in=self.textPreproc(text)
        predict_out=self.loaded_model.predict(predict_in)
        if predict_out > 0.5:
            predict_label = '긍정'
        else :
            predict_label = '부정'
        return predict_out, predict_label

    def print_summary(self):
        print(self.loaded_model.summary())

    
if __name__ == '__main__':
    mymodel = MyModel('./model/model_file.h5')
    mymodel.print_summary()
    print(mymodel.predict('엘사는 예전보다 더 강한 여자가 되어 있었다.'))
