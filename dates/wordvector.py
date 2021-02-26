#!/usr/bin/env python
# coding: utf-8

# In[1]:


import jieba
import pandas as pd
import os
import gensim
import numpy as np
from gensim.models.doc2vec import Doc2Vec


# In[2]:


def cut_sentence(text):
    stop_list = [line[:-1]for line in open(r'C:\Users\aner9\Desktop\大创\stopwords.txt')]
    result=[]
    for each in text:
        each_cut = jieba.cut(each)
        each_split = ' '.join(each_cut).split()
        each_result = [word for word in each_split if word not in stop_list]
        result.append(' '.join(each_result))
    return result


# In[3]:


def X_train(cut_sentence):
    x_train = []
    for i,text in enumerate(cut_sentence):
        word_list = text.split(' ')
        l = len(word_list)
        word_list[l-1] = word_list[l-1].strip()
        document = TaggededDocument(word_list, tags=[i])
        x_train.append(document)
    return x_train


# In[4]:


def train(x_train, size=300):
    model = Doc2Vec(x_train, min_count = 1,window = 3,vector_size = size,sample=1e-3,negative =5,workers=4)
    model.train(x_train, total_examples=model.corpus_count,epochs=10 )
    return model


# In[51]:


path = '20190901'
path_list = os.listdir(path)
path_list 
for filename in path_list:
    print(filename)
    print(os.path.join(path,filename))
    f = open(os.path.join(path,filename))
    df_train = pd.read_csv(f)
    text = list(df_train['Comment'].astype(str))
    sentence_cut = cut_sentence(text)
    TaggededDocument = gensim.models.doc2vec.TaggedDocument
    trainingword = X_train(sentence_cut)
    mod = train(trainingword)
    comment_matrix = np.zeros((len(sentence_cut),300))

    for row,text in enumerate(sentence_cut):
        word_list = text.split(' ')
        l = len(word_list)
        i = 0
        for element in word_list:
            comment_matrix[[row]] = comment_matrix[[row]] + mod[word_list[i]]
            i = i+1
        comment_matrix[[row]] = comment_matrix[[row]]/l    
   
    np.savetxt('result\\'+filename, comment_matrix, delimiter = ',')


# In[ ]:


np.savetxt('result\\' + filename, comment_matrix, delimiter = ',')

