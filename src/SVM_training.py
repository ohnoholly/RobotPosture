import numpy as np
from matplotlib import pyplot as plt
from sklearn import manifold
from sklearn import metrics
from sklearn import cross_validation
import os.path
from os import walk
import random
from numpy.random import permutation
import csv
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score

digits= np.genfromtxt('posture_data.csv',delimiter=",")

post = np.zeros((6,26))
for i in range (0,6):
    post[i,:] = digits [i+1,:]



#print post



scale = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]

var_post = np.zeros((6000,27))
for i in range (0,6):
    for j in range (0,26):
        var_post[i*1000:(i+1)*1000,j] = np.random.normal(post[i][j],scale[j],1000)
    for k in range (0,1000):
        var_post[i*1000+k,26]=i+1

var_post=permutation(var_post)

target=np.zeros((6000,1))
target=var_post[:,26]




n_samples = len(var_post)
data = var_post.reshape((n_samples, -1))
fnData = data
fnDigits = var_post
split = 0.7
percentSplit = split
nSamples = n_samples
def holdOut(fnDigits,fnData,nSamples,percentSplit=0.8):
    n_trainSamples = int(nSamples*percentSplit)
    trainData = fnData[:n_trainSamples,0:26]
    trainLabels = target[:n_trainSamples]
    
    testData = fnData[n_trainSamples:,0:26]
    expectedLabels = target[n_trainSamples:]
    return trainData, trainLabels, testData, expectedLabels

trainData, trainLabels, testData, expectedLabels = holdOut(fnDigits, fnData, nSamples, percentSplit)




clf_svm = LinearSVC()
clf_svm.fit(trainData, trainLabels)
predictedLabels = clf_svm.predict(testData)
acc_svm = accuracy_score(expectedLabels, predictedLabels)
print("Classification report for classifier %s: \n %s \n"
      % ('SVM', metrics.classification_report(expectedLabels, predictedLabels)))
print("Confusion matrix:\n %s" % metrics.confusion_matrix(expectedLabels, predictedLabels))


print "Linear SVM accuracy: ", acc_svm



# Display classification results
kFold = 6
scores = cross_validation.cross_val_score(clf_svm, fnData, target, cv=kFold)
print(scores)



