# -*- coding: utf-8 -*-
"""
Created on Sun Oct 09 12:57:16 2016

@author: Jane
"""

import pandas
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

from sklearn.grid_search import GridSearchCV
from sklearn import cross_validation

from pprint import pprint
from time import time
import matplotlib.pyplot as plt
import numpy as np
#from sklearn.cross_validation import cross_val_predict
#%%

dataset = pandas.read_csv('training_data.csv')
y = dataset['is_churner_uninstalled']
features = list(dataset.columns.values)
features.remove('Game')
features.remove('Unnamed: 0')
features.remove('Unnamed: 0.1')
features.remove('device_id')
features.remove('is_churner_uninstalled')
features.remove('is_churner_inactive')
#X = preprocessing.normalize(dataset[features])
X = dataset[features]
num_folds = 5
num_instance = len(X)
seed = 1
#%%
models = [
    ('lr', LogisticRegression()),
    ('rfc', RandomForestClassifier(random_state = seed)),
    #('svc', SVC()),
    ('nb', GaussianNB())
]


results = []
names = []
scoring = 'accuracy'
for name, model in models:
    t0 = time()
    kfold = cross_validation.KFold(n = num_instance, n_folds = num_folds, random_state = seed)
    cv_results = cross_validation.cross_val_score(model, X, y, cv=kfold, scoring = scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)
    print("done in %0.3fs" % (time() - t0))

# boxplot algorithm comparison
fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()

#lr: 0.761880 (0.007447)
#done in 0.890s
#rfc: 0.745029 (0.004945)
#done in 1.170s
#svc: 0.758848 (0.019705)
#done in 23.516s
#nb: 0.558798 (0.030679)
#done in 0.062s

#%%
new_models = [
    ('lr', LogisticRegression()),
    ('rfc', RandomForestClassifier())
]

lr_grid = {'C': [0.01, 0.1, 1, 10, 100]}
rfc_grid = {'n_estimators': [5, 10 ,50], 
             'min_samples_leaf': [1, 20, 50, 80],
             'max_features': [None, 'sqrt', 0.2]
             }
parameters = {'lr': lr_grid,
              'rfc': rfc_grid}
result = {}
for name, model in new_models:
    model_parameters = parameters[name]
    grid_search = GridSearchCV(model, model_parameters, cv = num_folds)
    print("Performing grid search for %s" %(name))
    print("parameters:")
    pprint(model_parameters)
    t0 = time()
    grid_search.fit(X,y)
    print("done in %0.3fs" % (time() - t0))
    
    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    result[name] = best_parameters
    for param_name in sorted(model_parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))

#Performing grid search for lr
#parameters:
#{'C': [0.01, 0.1, 1, 10, 100]}
#done in 1.786s
#Best score: 0.764
#Best parameters set:
#	C: 0.1
#Performing grid search for rfc
#parameters:
#{'max_features': [None, 'sqrt', 0.2],
# 'min_samples_leaf': [1, 20, 50, 80],
# 'n_estimators': [5, 10, 50]}
#done in 90.812s
#Best score: 0.776
#Best parameters set:
#	max_features: None
#	min_samples_leaf: 50
#	n_estimators: 5

#%%
rfc_para = result['rfc']
best_model = RandomForestClassifier(max_features = rfc_para['max_features'], min_samples_leaf = rfc_para['min_samples_leaf'], n_estimators = rfc_para['n_estimators'])
best_model.fit(X, y)
importances = best_model.feature_importances_
std = np.std([best_model.feature_importances_ for tree in best_model.estimators_],axis=0)
indices = np.argsort(importances)[::-1]
indices_features = map(lambda x: features[x],indices)

from sklearn.metrics import confusion_matrix
y_p = best_model.predict(X)
print confusion_matrix(y_p,y)
# Print the feature ranking
print("Feature ranking:")

for f in range(X.shape[1]):
    print("%d. %s (%f)" % (f + 1, indices_features[f], importances[indices[f]]))


# Plot the feature importances of the forest
plt.close('all')
fig_importance = plt.figure()
plt.title("Feature importances")
plt.bar(range(X.shape[1]), importances[indices],
       color="r", yerr=std[indices], align="center")
plt.xticks(range(X.shape[1]), indices_features)
plt.xlim([-1, X.shape[1]])
fig_importance.autofmt_xdate()
plt.show()
#%%
lr_para = result['lr']
best_model_2 = LogisticRegression(C = lr_para['C'])
best_model_2.fit(X,y)
coef = best_model_2.coef_
for i in range(len(features)):
    print ("%s (%f)" % (features[i], coef[0,i]))