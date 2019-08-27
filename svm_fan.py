#!/usr/bin/env python3

from sklearn.svm import SVC
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

FEA_type = [['Xstd',    'Ystd',     'Zstd'  ],
            ['Xcrest',  'Ycrest',   'Zcrest'],
            ['Xkurtosis','Ykurtosis','Zkurtosis']]


lev_color = ['r','g','b']

#svm = SVC(kernel = 'linear', probability = True)


# load fan data
fan_data_dir = '/home/vandine/MachineAnalyzer/data/fan/'

# load balanced data
from DataIO import ImportFeaData, FEA_ColumnDict


      
balanced_lev1 = np.array(ImportFeaData(fan_data_dir+'Balanced/FEA_LV1.bin'))
balanced_lev2 = np.array(ImportFeaData(fan_data_dir+'Balanced/FEA_LV2.bin'))
balanced_lev3 = np.array(ImportFeaData(fan_data_dir+'Balanced/FEA_LV3.bin'))


unbalanced_lev1 = np.array(ImportFeaData(fan_data_dir+'Unbalanced/FEA_LV1.bin'))
unbalanced_lev2 = np.array(ImportFeaData(fan_data_dir+'Unbalanced/FEA_LV2.bin'))
unbalanced_lev3 = np.array(ImportFeaData(fan_data_dir+'Unbalanced/FEA_LV3.bin'))

balanced = np.array([])
balanced = np.array([balanced_lev1, balanced_lev2, balanced_lev3])

unbalanced = np.array([])
unbalanced = np.array([unbalanced_lev1, unbalanced_lev2, unbalanced_lev3])

ndata_balanced = [len(balanced_lev1), len(balanced_lev2), len(balanced_lev3)]
ndata_unbalanced = [len(unbalanced_lev1), len(unbalanced_lev2), len(unbalanced_lev3)]

'''
for lev_index in range(3):

    plt.plot( [lev_index+1] * ndata_unbalanced[lev_index], 
              unbalanced[lev_index][:,FEA_ColumnDict[FEA_type[0]]], 
              'bo')
    plt.plot( [lev_index+1] * ndata_unbalanced[lev_index], 
              unbalanced[lev_index][:,FEA_ColumnDict[FEA_type[1]]], 
              'bs')
    plt.plot( [lev_index+1] * ndata_unbalanced[lev_index], 
              unbalanced[lev_index][:,FEA_ColumnDict[FEA_type[2]]], 
              'b^')
    
    plt.plot( [lev_index+1] * ndata_balanced[lev_index], 
             balanced[lev_index][:,FEA_ColumnDict[FEA_type[0]]], 
             'ro')
    plt.plot( [lev_index+1] * ndata_balanced[lev_index], 
             balanced[lev_index][:,FEA_ColumnDict[FEA_type[1]]], 
             'rs')
    plt.plot( [lev_index+1] * ndata_balanced[lev_index], 
              balanced[lev_index][:,FEA_ColumnDict[FEA_type[2]]], 
              'r^')

plt.xlim(left=0,right=4)
'''

'''
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

FEA_index = 2
for lev_index in range(3):
    ax.scatter( balanced[lev_index][:,FEA_ColumnDict[FEA_type[FEA_index][0]]], 
                balanced[lev_index][:,FEA_ColumnDict[FEA_type[FEA_index][1]]], 
                balanced[lev_index][:,FEA_ColumnDict[FEA_type[FEA_index][2]]], 
                marker = 'o',
                c = lev_color[lev_index])
    ax.scatter( unbalanced[lev_index][:,FEA_ColumnDict[FEA_type[FEA_index][0]]], 
                unbalanced[lev_index][:,FEA_ColumnDict[FEA_type[FEA_index][1]]], 
                unbalanced[lev_index][:,FEA_ColumnDict[FEA_type[FEA_index][2]]], 
                marker = '^',
                c = lev_color[lev_index])


ax.set_xlabel(FEA_type[FEA_index][0])
ax.set_ylabel(FEA_type[FEA_index][1])
ax.set_zlabel(FEA_type[FEA_index][2])
plt.show()
'''


X_train = np.array([])
Y_train = np.array([])
for lev_index in range(3):
    X_train = np.append( X_train, balanced[lev_index])
    Y_train = np.append( Y_train, [0]*len(balanced[lev_index]))
    X_train = np.append( X_train, unbalanced[lev_index])
    Y_train = np.append( Y_train, [1]*len(unbalanced[lev_index]))

X_train = X_train.reshape(int(len(X_train)/26),26)


#SVM
clf = SVC(kernel='linear', C=1.0)
clf.fit(X_train, Y_train)


#print(clf.support_vectors_.shape, clf.support_vectors_[4][25])
#print(clf.coef_.shape, clf.intercept_)

#print(X_train.shape[0])
#exit()


true = 0
TP = 0
FP = 0

false = 0
TN = 0
FN = 0

for i in range(X_train.shape[0]):
    predict = clf.coef_.dot(X_train[i,:]) + clf.intercept_
    if predict > 0.: 
        true += 1
        if Y_train[i] == 1:
            TP += 1
        else:
            FP += 1
    else:
        false += 1
        if Y_train[i] == 0:
            TN += 1
        else:
            FN += 1
        
print('True  Positive:',TP/true)
print('False Positive:',FP/true)
print('True  Negative:',TN/false)
print('False Negative:',FN/false)



'''
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

# Plot also the training points
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm)
plt.xlabel('Sepal length')
plt.ylabel('Sepal width')
plt.xlim(xx.min(), xx.max())
plt.ylim(yy.min(), yy.max())
plt.xticks(())
plt.yticks(())
plt.title(titles[i])

plt.show()
'''




