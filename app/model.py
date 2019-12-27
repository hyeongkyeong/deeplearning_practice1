#-*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from konlpy.tag import Okt
from tensorflow import keras
from keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
import re
import json


class MyModel:
    loaded_model=Sequential()

    def __init__(self, loaded_model):
        self.loaded_model=keras.models.load_model(loaded_model)
        print('[model.py] Model loaded successfully..')

    def textPreproc(self, text_in):
        ''' Delete Special Character '''
        print('[model.py] Deleting Special Character..')
        temp_text=re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z ]","", str(text_in))
        print('[model.py] >>> ', temp_text)
    
        ''' Tockenization and Delete Stopword '''
        print('[model.py] Tockenization Special Character..')
        okt = Okt()
        okt.morphs
        tocken_text=[]
        tocken_text=okt.morphs(temp_text, stem=True) 
        print('[model.py] >>> ', tocken_text)
    
        ''' Delete Stopword '''
        print('[model.py] Deleting Stopword..')
        stopwords=['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다'] # Stopword List
        tocken_text=[word for word in tocken_text if not word in stopwords] 
        tocken_text = [tocken_text]
        print('[model.py] >>> ', tocken_text)

        ''' Load token '''
        print('[model.py] Loading tockenized data..')
        with open('./../model/tokenizer.json') as f:
            data = json.load(f)
            tokenizer = tokenizer_from_json(data)
        tocken_text = tokenizer.texts_to_sequences(tocken_text)
        print('[model.py] >>> ', tocken_text)
        
        ''' Array Size Synch '''
        print('[model.py] Syncing array size..')
        max_array_len=30
        preprocessed_data = pad_sequences(tocken_text, maxlen=max_array_len)
        print('[model.py] >>> ', preprocessed_data)
        
        print('[model.py] Preprocessing Done!')
        return preprocessed_data
    
    def predict(self, text):
        print('[model.py] Start Predicting~!')
        print('[model.py] <<< ', text)
        predict_in=self.textPreproc(text)
        predict_out=self.loaded_model.predict(predict_in)
        if predict_out > 0.5:
            predict_label = 'Positive'
        else :
            predict_label = 'Negative'
        print('[model.py] Predicting Done!:', float(predict_out),',',predict_label)
        return predict_out, predict_label

    def print_summary(self):
        print(self.loaded_model.summary())

    
if __name__ == '__main__':
    mymodel = MyModel('./../model/model_file.h5')
    mymodel.print_summary()
    # Predict Example
    result=mymodel.predict('ㄴㄹㅇㄴㄷㄹㄴㄷㄹ')
    print("예측값: ",float(result[0]),", 판단: ",result[1])