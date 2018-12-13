# liuchang 2018.11.6
import numpy as np
import jieba
import json
import jieba.posseg as pseg
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from scipy import io, sparse
import cPickle as pickle
from sklearn.decomposition import NMF
from sklearn.decomposition import PCA
class TfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        def analyzer(doc):
            words = pseg.cut(doc)
            new_doc = ''.join(w.word for w in words if w.flag != 'x')
            words = jieba.cut(new_doc)
            return words
        return analyzer
def data_preprocessing(dataset_path):
    data = []
    label = []
    with open(dataset_path + '/message.txt', 'r') as f:
        
        #print len(lines)
        for i in range(50000):
            line = f.readline()
            message = line.split('\t')
            label.append(message[0])
            data.append(message[1])
    vector = get_vector(data)
    print('get_vector done!')
    train_data, test_data, train_label, test_label = split_data(vector,label)

    with open('model50000/train_label.json','w') as f0:
        json.dump(train_label,f0)
    io.mmwrite('model50000/train_data', train_data)
    with open('model50000/test_label.json','w') as f1:
        json.dump(test_label,f1)
    io.mmwrite('model50000/test_data', test_data)
'''
    vector_r = dim_reduction(vector)
    train_data_r, test_data_r, train_label_r, test_label_r = split_data(vector,label)

    with open('train_label_r.json','w') as f0:
        json.dump(train_label_r,f0)
    io.mmwrite('train_data_r', train_data_r)
    with open('test_label_r.json','w') as f1:
        json.dump(test_label_r,f1)
    io.mmwrite('test_data_r', test_data_r)
'''
def get_vector(data):

    #with open('data.json','w') as f0:
    #    train_data = json.load(f0)
    #with open('test_data.json','w') as f1:
    #    test_data = json.load(f1)

    vectorizer = TfidfVectorizer()
    train_vector = vectorizer.fit_transform(data)
    pickle.dump(vectorizer, open("model50000/tfidf_model", 'wb'))
    #test_vector = vectorizer.fit_transform(test_data)
    return train_vector
    #io.mmwrite('word_vector.mtx', train_vector)
    #io.mmwrite('test_word_vector.mtx', test_vector)

def dim_reduction(data, type='pca'):
    if type == 'pca':
        n_components = 1000
        pca = PCA(n_components=n_components)
        pca.fit(data.todense())
    
        return sparse.csr_matrix(pca.transform(data))
    if type =='nmf':
        n_components = 1000
        nmf = NMF(n_components=n_components)
        nmf.fit(data.todense())
    
        return sparse.csr_matrix(nmf.transform(data))
    
def split_data(data, label):
    train_data, test_data, train_label, test_label = train_test_split(data, label, test_size=0.1, random_state=20)
    return train_data, test_data, train_label, test_label

if __name__ == '__main__':
    data_preprocessing('.')
    