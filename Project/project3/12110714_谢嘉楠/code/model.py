
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedShuffleSplit #分层交叉验证
import joblib
from sklearn.metrics import roc_auc_score,precision_recall_curve,classification_report,roc_curve

#读取数据
label = pd.read_csv(r'F:\Artificial Intelligence\Project\project3\data\trainlabel.txt',header = None, names=["income"])
traindata= pd.read_csv(r'F:\Artificial Intelligence\Project\project3\data\traindata.csv')



continuous_columns=['age','fnlwgt','education.num','capital.gain','capital.loss','hours.per.week']
discrete_columns=['workclass','education','marital.status','occupation','relationship','race','sex','native.country']

encode_traindata = pd.get_dummies(traindata,columns=discrete_columns) #离散型特征独热编码
traindata_x=encode_traindata
traindata_y=label.values #获取字段值
#连续型字段数据标准正态归一化（用于消除奇异值）
mean=traindata_x[continuous_columns].mean()
std=traindata_x[continuous_columns].std()
normal=(traindata_x[continuous_columns]-mean)/std

traindata_x=traindata_x.drop(columns=continuous_columns)
traindata_x=pd.concat([traindata_x,normal],axis=1)
traindata_x=traindata_x.values
#分层交叉训练
sss=StratifiedShuffleSplit(n_splits=2,train_size=0.75)
for train_index,test_index in sss.split(traindata_x,traindata_y):
    trainx,testx = traindata_x[train_index],traindata_x[test_index]
    trainy,testy = traindata_y[train_index],traindata_y[test_index]

#随机梯度下降分类器（线性）
lr=SGDClassifier(loss='log',max_iter=100)
lr.fit(trainx,trainy)

pred_lr=lr.predict_log_proba(testx)[:,1]
pred_labels_lr=lr.predict(testx)

joblib.dump(lr,'save/lr.pkl')#导出lr模型

print(roc_auc_score(testy,pred_lr))
print(classification_report(testy,pred_labels_lr))

#梯度上升分类器（非线性）
gbc=GradientBoostingClassifier(max_depth=6)
gbc.fit(trainx,trainy)
gbc.score(testx,testy)

pred_gbc=gbc.predict_proba(testx)[:,1]
pred_labels_gbc=gbc.predict(testx)

joblib.dump(gbc,'save/gbc.pkl')#导出gbc模型

print(roc_auc_score(testy,pred_gbc))
print(classification_report(testy,pred_labels_gbc))

#PR曲线
precision,recall,_ = precision_recall_curve(testy,pred_gbc)
plt.plot(recall,precision)
plt.xlabel('recall')
plt.ylabel('precision')
plt.show()

#ROC曲线
fpr,tpr,_ = roc_curve(testy,pred_gbc)
plt.plot(fpr,tpr)
plt.xlabel('fpr')
plt.ylabel('tpr')
plt.show()
