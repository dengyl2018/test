#coding=utf-8
"""
https://www.cnblogs.com/wsine/p/5180343.html
https://www.cnblogs.com/youngsea/p/9321784.html
https://www.cnblogs.com/wjq-Law/p/9779657.html
"""


import pdb
import pandas
import numpy
import matplotlib.pyplot as plt
import operator
import time


LINE_OF_DATA = 6
LINE_OF_TEST = 4

def createTrainDataSet():
    trainDataMat = [[1, 1, 4], 
                    [1, 2, 3], 
                    [1, -2, 3], 
                    [1, -2, 2], 
                    [1, 0, 1], 
                    [1, 1, 2]]
    trainShares = [1, 1, 1, 0, 0,  0]
    return trainDataMat, trainShares

def createTestDataSet():
    testDataMat = [[1, 1, 1], 
                   [1, 2, 0], 
                   [1, 2, 4], 
                   [1, 1, 3]]
    return testDataMat

def autoNorm(dataSet):
    pdb.set_trace()
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = numpy.zeros(numpy.shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - numpy.tile(minVals, (m, 1))
    normDataSet = normDataSet / numpy.tile(ranges, (m, 1))
    return normDataSet[:LINE_OF_DATA], normDataSet[LINE_OF_DATA:]

def sigmod(inX):
    return 1.0 / (1 + numpy.exp(-inX))

def gradAscent(dataMatIn, classLables, alpha=0.01, maxCycles=1000):
    # pdb.set_trace()
    dataMatrix = numpy.mat(dataMatIn)
    labelMat = numpy.mat(classLables).transpose()
    m, n = numpy.shape(dataMatrix)
    weights = numpy.ones((n, 1))
    for k in range(maxCycles):
        h = sigmod(dataMatrix * weights)
        error = labelMat - h
        weights = weights + alpha * dataMatrix.transpose() * error
        # print "error : %s " % error
    return weights

def plotBestFit(weights):
    # pdb.set_trace()
    dataMat, lableMat = createTrainDataSet()
    dataArr = numpy.array(dataMat)
    n = numpy.shape(dataArr)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(lableMat[i]) == 1:
            xcord1.append(dataArr[i, 1])
            ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1])
            ycord2.append(dataArr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = numpy.arange(-3.0, 3.0, 0.1)
    # pdb.set_trace()
    y = (-weights[0] - weights[1] * x) / weights[2]
    ax.plot(x, y)
    plt.xlabel('X1'); plt.ylabel('X2')
    plt.show()

def classifyVector(inX, weights):
    return 1 if sigmod(sum(inX * weights)) > 0.5 else 0

def classifyAll(dataSet, weights):
    predict = []
    for vector in dataSet:
        predict.append(classifyVector(vector, weights))
    return predict


def sklearnlib(dataMatIn, classLables, dataMatTest, y_test):
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.linear_model import stochastic_gradient
    from sklearn.metrics import classification_report
    ss = StandardScaler()
    x_train = ss.fit_transform(numpy.mat(dataMatIn))
    y_train = numpy.mat(classLables).transpose()
    x_test = ss.transform(numpy.mat(dataMatTest))
    # pdb.set_trace()
    ### LR
    lr = LogisticRegression()
    lr.fit(x_train, y_train)
    lr_y_predict = lr.predict(x_test)
    print "LR predict: \n", lr_y_predict
    # print "Accuracy of LR Classifier: %f" % lr.score(x_test, y_test)
    # print classification_report(y_test, lr_y_predict, target_names=["Begin", "Malignant"])
    ### SGD
    sgdc=stochastic_gradient.SGDClassifier(max_iter=5)  # 初始化分类器
    sgdc.fit(x_train, y_train)
    sgdc_y_predit=sgdc.predict(x_test)
    print "SGD predict: \n", sgdc_y_predit
    # print 'Accuarcy of SGD Classifier:', sgdc.score(x_test, y_test)
    # print classification_report(y_test, sgdc_y_predit, target_names=['Benign','Malignant'])

def main():
    trainDataSet, trainShares = createTrainDataSet()
    testDataSet = createTestDataSet()
    # trainDataSet, testDataSet = autoNorm(numpy.vstack((numpy.mat(trainDataSet), numpy.mat(testDataSet))))
    # regMatrix = gradAscent(trainDataSet, trainShares, 0.01, 600)
    # print "regMatrix = \n", regMatrix
    # # [[-2.7205211 ]
    # # [ 0.19112108]
    # # [ 1.23590529]]
    # # plotBestFit(regMatrix.getA())
    # predictShares = classifyAll(testDataSet, regMatrix)
    # print "predictResult: \n", predictShares
    ######
    y_test = [0, 0, 1, 1]
    sklearnlib(trainDataSet, trainShares, testDataSet, y_test)

if __name__ == "__main__":
    start = time.clock()
    main()
    end = time.clock()
    print "cost : %s" % str(end - start)