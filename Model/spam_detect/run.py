from data import data_preprocessing, get_vector, dim_reduction, split_data
from classifiers import logistic_regression, svm, GBDT, decision_tree, perceptron # knn is removed
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import jieba
import jieba.posseg as pseg
import argparse
import cPickle as pickle
from sklearn import metrics 
import json
from scipy import io
import time
import data

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
    parser.add_argument('command', action= 'store', help= 'Determines what to do: train and test ,or inference')
    parser.add_argument('--classifier', type=str, action= 'store', default = 'P')
    args = parser.parse_args()
    
    if args.command.lower() == 'train':

        #print('data data_preprocessing...')
        #data_preprocessing('.')
        
        print('training ...')
        with open('model50000/train_label.json') as f0:
            train_label = json.load(f0)
        train_data = io.mmread('model50000/train_data.mtx')

        classifiers = { 
                        #'KNN':knn,  
                        'LR':logistic_regression,    
                        'DT':decision_tree, 
                        'GBDT':GBDT,
                        'SVM':svm,
                        'P':perceptron
        }  
        train_classifiers = ['SVM']
        for classifier in train_classifiers:
            start_time = time.time()
            model = classifiers[classifier](train_data,train_label)
            pickle.dump(model,open('model50000/'+classifier, 'wb'))
            print(classifier+' done!')
            print('took %fs!'%(time.time()-start_time))
        print('train done!')
 
    
    if args.command.lower() == 'test':
        print('test start...')
        classifier = args.classifier
        with open('model50000/test_label.json') as f0:
            test_label = json.load(f0)
        test_data = io.mmread('model50000/test_data.mtx')
        model = pickle.load(open('model50000/'+classifier, 'rb'))
        start_time = time.time()   
        
        predict = model.predict(test_data)
        precision = metrics.precision_score(test_label, predict, pos_label= u'1') 
        recall = metrics.recall_score(test_label, predict, pos_label= u'1')  
        print 'precision: %.2f%%, recall: %.2f%%' % (100 * precision, 100 * recall)  
        accuracy = metrics.accuracy_score(test_label, predict)  
        print 'accuracy: %.2f%%' % (100 * accuracy)
        print 'test took %fs!' % (time.time() - start_time)

        print('RESULT')
        print(metrics.classification_report(test_label, predict))

    if args.command.lower() == 'inference':

        classifier = args.classifier
        model = pickle.load(open('model50000/'+classifier, 'rb'))
        vec_tfidf = pickle.load(open("model50000/tfidf_model", 'rb')) 
        while True:
            inference_data = raw_input('input text:')
            if inference_data == 'exit':
                break
            inference_data = [inference_data]
            inference_vector = vec_tfidf.transform(inference_data)
            start_time = time.time()   
            predict = model.predict(inference_vector)
            #print (predict)
            if predict == '0':
                print('Not spam!')
            elif predict == '1':
                print('Is spam')
        

