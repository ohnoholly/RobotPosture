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

def trainModel(inputData):
    digits= np.genfromtxt('posture_simple_data.csv',delimiter=",")

#print digits

    post = np.zeros((6,11))
    for i in range (0,6):
        post[i,:] = digits [i+1,:]



#print post



    scale = [5,5,5,5,5,5,5,5,0.01,0.01,0.01]
    var_post = np.zeros((6000,12))
    for i in range (0,6):
        for j in range (0,11):
            var_post[i*1000:(i+1)*1000,j] = np.random.normal(post[i][j],scale[j],1000)
        for k in range (0,1000):
            var_post[i*1000+k,11]=i+1

    var_post=permutation(var_post)

    #print var_post

    target=np.zeros((6000,1))
    target=var_post[:,11]




    n_samples = len(var_post)
    data = var_post.reshape((n_samples, -1))
    fnData = data
    fnDigits = var_post
    split = 0.7
    percentSplit = split
    nSamples = n_samples
    def holdOut(fnDigits,fnData,nSamples,percentSplit=0.8):
        n_trainSamples = int(nSamples*percentSplit)
        trainData = fnData[:n_trainSamples,0:11]
        trainLabels = target[:n_trainSamples]
    
        testData = fnData[n_trainSamples:,0:11]
        expectedLabels = target[n_trainSamples:]
        return trainData, trainLabels, testData, expectedLabels

    trainData, trainLabels, testData, expectedLabels = holdOut(fnDigits, fnData, nSamples, percentSplit)




    clf_svm = LinearSVC()
    clf_svm.fit(trainData, trainLabels)

    testData = np.array(inputData)
    expectedLabels = np.array([1])
    #print testData
    #print expectedLabels
   

    predictedLabels = clf_svm.predict(testData)
    #print predictedLabels
    #raw_input()
    acc_svm = accuracy_score(expectedLabels, predictedLabels)
    #print("Classification report for classifier %s: \n %s \n"
    #      % ('SVM', metrics.classification_report(expectedLabels, predictedLabels)))
    #print("Confusion matrix:\n %s" % metrics.confusion_matrix(expectedLabels, predictedLabels))


    #print "Linear SVM accuracy: ", acc_svm


    # Display classification results
    #kFold = 6
    #scores = cross_validation.cross_val_score(clf_svm, fnData, target, cv=kFold)
    #print(scores)
    return predictedLabels, post

if __name__ == '__main__':
    trainModel(1)



