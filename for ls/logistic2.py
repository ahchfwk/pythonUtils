from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import leastsq
from scipy.optimize import leastsq
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report 
from sklearn.metrics import precision_recall_curve, roc_curve, auc 

data = pd.read_csv('HTRU_2.csv', sep=',', \
    skiprows=[2], names=['score1','score2','score3','score4','score5','score6','score7','score8','result'])
score_data = data.loc[:,['score1','score2','score3','score4','score5','score6','score7','score8']]
result_data = data.result


tem = data.values  # 将series类型转化成list类型方便操作
PosiData = []
NegaData = []
for item in tem:
        if item[8] == 0:
            NegaData.append(item)
        else:
            PosiData.append(item)

for n in range(1,11):
    print '--------------正负样本比为1：'+str(n)+'时：'
    tem = PosiData + NegaData[:len(PosiData)*n]
    data = pd.DataFrame(tem)
    score_data = data.loc[:, [0,1,2,3,4,5,6,7]]
    # print score_data
    result_data = data.loc[:,8]
    # print result_data

    p = 0
    for i in xrange(10):
        x_train, x_test, y_train, y_test = \
            train_test_split(score_data, result_data, test_size = 0.2)
        model = LogisticRegression(C=1e9)
        model.fit(x_train, y_train)
        predict_y = model.predict(x_test)
        p += np.mean(predict_y == y_test)


    # 模型表现
    answer = model.predict_proba(x_test)[:, 1]
    precision, recall, thresholds = precision_recall_curve(y_test, answer)      
    report = answer > 0.5  
    print(classification_report(y_test, report, target_names = ['neg', 'pos']))  
    print("average precision:", p/100)  
