from classifiers import logistic_regression, svm, GBDT, decision_tree, perceptron # knn is removed
import argparse
import cPickle as pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba
import jieba.posseg as pseg
import argparse
import cPickle as pickle
from scipy import io
import time

# copy from run.py 

class TfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        def analyzer(doc):
            words = pseg.cut(doc)
            new_doc = ''.join(w.word for w in words if w.flag != 'x')
            words = jieba.cut(new_doc)
            return words
        return analyzer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'SVM, LR, P, DT, GBDT')
    parser.add_argument('--classifier', type=str, action= 'store', default = 'P')
    parser.add_argument('--msg', type=str, action= 'store', default='')
    args = parser.parse_args()

    classifier = args.classifier
    model = pickle.load(open('model50000/'+classifier, 'rb'))
    vec_tfidf = pickle.load(open("model50000/tfidf_model", 'rb')) 
    # remove while True
    inference_data = args.msg
    inference_data = [inference_data]
    inference_vector = vec_tfidf.transform(inference_data)
    start_time = time.time()   
    predict = model.predict(inference_vector)
    # print(predict)
    if predict == '0':
        print(0)
    elif predict == '1':
        print(1)
