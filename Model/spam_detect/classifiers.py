from sklearn.neighbors import KNeighborsClassifier  #knn

from sklearn.model_selection import GridSearchCV  
from sklearn.svm import SVC  #SVM
from sklearn.linear_model import LogisticRegression #Logistic Regression
from sklearn.linear_model import Perceptron #Perceptron

from sklearn.tree import DecisionTreeClassifier #decision tree 
from sklearn.ensemble import GradientBoostingClassifier #GBDT


from scipy import io

#def knn(data,label):
#    model = KNeighborsClassifier()  
#    model.fit(data, label)  
#    return model 
def svm(data,label):
    model = SVC(kernel='rbf', probability=True)  
    param_grid = {'C': [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000], 'gamma': [0.001, 0.0001]}  
    grid_search = GridSearchCV(model, param_grid, n_jobs = 1, verbose=1)  
    grid_search.fit(data, label)  
    best_parameters = grid_search.best_estimator_.get_params()  
  
    model = SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True)  
    #model = SVC(kernel='rbf', C=10, gamma=0.001, probability=True)  
    model.fit(data, label) 
    return model

def logistic_regression(data,label):
    model = LogisticRegression()
    model.fit(data, label)
    return model

def perceptron(data,label):
    model = Perceptron()  
    model.fit(data, label)  
    return model 

def decision_tree(data,label):
    model = DecisionTreeClassifier()  
    model.fit(data, label)  
    return model 

def GBDT(data,label):
    model = GradientBoostingClassifier()
    model.fit(data,label)
    return model
