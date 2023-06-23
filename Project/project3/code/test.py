import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.metrics import roc_auc_score,precision_recall_curve,classification_report,roc_curve

testdata = pd.read_csv(r'F:\Artificial Intelligence\Project\project3\data\testdata.csv')
traindata= pd.read_csv(r'F:\Artificial Intelligence\Project\project3\data\traindata.csv')
continuous_columns=['age','fnlwgt','education.num','capital.gain','capital.loss','hours.per.week']
discrete_columns=['workclass','education','marital.status','occupation','relationship','race','sex','native.country']

encode_testdata = pd.get_dummies(testdata,columns=discrete_columns) #离散型特征热编码
encode_traindata = pd.get_dummies(traindata,columns=discrete_columns)
encode_reshape = encode_traindata.align(encode_testdata, join='left', fill_value=0,fill_axis=1)[0]
testdata_x = encode_reshape

mean=testdata_x[continuous_columns].mean()
std=testdata_x[continuous_columns].std()
normal=(testdata_x[continuous_columns]-mean)/std


testdata_x=testdata_x.drop(columns=continuous_columns)
testdata_x=pd.concat([testdata_x,normal],axis=1)
# print(testdata_x.isna().sum().sum())
testdata_x=testdata_x.values

# lr = joblib.load('save/lr.pkl')
# lr_pred = lr.predict(testdata_x)
# np.savetxt(r'F:\Artificial Intelligence\Project\project3\code\testlabel.txt',lr_pred,fmt='%d')
# print(lr_pred)

gbc = joblib.load('save/gbc.pkl')
gbc_pred = gbc.predict(testdata_x)
np.savetxt(r'F:\Artificial Intelligence\Project\project3\code\testlabel.txt',gbc_pred,fmt='%d')