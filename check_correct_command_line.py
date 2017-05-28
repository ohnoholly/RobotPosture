import sys, getopt
import math


def correct(testingdata,standard_data,distance):
    err = []
    
    for i in range(len(testingdata)):
        err1 = abs(standard_data[i]-testingdata[i])/distance
        err.append(err1)
    max_err = max(err)
    for i in range(len(testingdata)):
        if (max_err == err[i]):
            print 'the #',i, 'err,  need to modify'


def check_if_is_right(testingdata,standardData):
    sum_distance = 0
    for i in range(len(standardData)):
        sum_distance +=(standardData[i]-testingdata[i])**2
        distance = math.sqrt(sum_distance)
    if (distance <= 0):
        print 'right'
    else :
        correct(testingdata,standardData,distance)


if __name__ == "__main__":

    print"Welcome IIS project, we are group 5"
    testingdata = [1,6]
    standardData = [2,3]
    check_if_is_right(testingdata, standardData)


