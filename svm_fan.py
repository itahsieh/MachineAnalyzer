#!/usr/bin/env python3

from sklearn.svm import SVC
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

FEA_type = [['Xstd',    'Ystd',     'Zstd'  ],
            ['Xcrest',  'Ycrest',   'Zcrest'],
            ['Xskewness','Yskewness','Zskewness'],
            ['Xkurtosis','Ykurtosis','Zkurtosis']]


lev_color = ['r','g','b']
lev_mark = ['o','^','s']

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
Spec_figsize = (12, 12)
Spec_dpi = 80
#plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)

fig = plt.figure(figsize=Spec_figsize, dpi=Spec_dpi)
ax = fig.add_subplot(111, projection='3d')

FEA_index = 3
for lev_index in range(3):
    ax.scatter( balanced[lev_index][:,FEA_ColumnDict[FEA_type[FEA_index][0]]], 
                balanced[lev_index][:,FEA_ColumnDict[FEA_type[FEA_index][1]]], 
                balanced[lev_index][:,FEA_ColumnDict[FEA_type[FEA_index][2]]],
                label = 'Balanced, Speed Level '+str(lev_index+1),
                marker = lev_mark[lev_index],
                c = 'navy')
    ax.scatter( unbalanced[lev_index][:,FEA_ColumnDict[FEA_type[FEA_index][0]]], 
                unbalanced[lev_index][:,FEA_ColumnDict[FEA_type[FEA_index][1]]], 
                unbalanced[lev_index][:,FEA_ColumnDict[FEA_type[FEA_index][2]]], 
                label = 'Unbalanced, Speed Level '+str(lev_index+1),
                marker = lev_mark[lev_index],
                c = 'darkorange')


ax.set_xlabel(FEA_type[FEA_index][0])
ax.set_ylabel(FEA_type[FEA_index][1])
ax.set_zlabel(FEA_type[FEA_index][2])
ax.legend(loc='upper right', shadow=True, fontsize='x-large')
plt.show()
exit()
'''





X_train = np.array([])
Y_train = np.array([])
for lev_index in range(3):
    X_train = np.append( X_train, balanced[lev_index])
    Y_train = np.append( Y_train, [0]*len(balanced[lev_index]))
    X_train = np.append( X_train, unbalanced[lev_index])
    Y_train = np.append( Y_train, [1]*len(unbalanced[lev_index]))

X_train = X_train.reshape(int(len(X_train)/26),26)




from sklearn.decomposition import PCA
pca = PCA(n_components=26)
pca.fit(X_train)
X_trans = pca.transform(X_train)

#print(pca.components_[0].dot(X_train[0,:]-pca.mean_))
#print(pca.explained_variance_)
#print(X_trans[0,:])

summation = 0.
weight = np.zeros(26)
for j in range(26):
    weight[j] =  pca.components_[0,j]
    weight[j] /= np.std(X_train[:,j])
    summation += np.abs(weight[j])
for j in range(8):
    wx = weight[j]/summation*100. 
    wy = weight[j+8]/summation*100.
    wz = weight[j+16]/summation*100.
    print('%.2f %.2f %.2f' % (wx,wy,wz))
print('%.2f' % (weight[24]/summation*100. ))
print('%.2f' % (weight[25]/summation*100. ))
exit()



#print(list(FEA_ColumnDict.keys()))
#exit()
import pandas as pd
target = ['']*len(Y_train)
for i in range(len(target)):
    if Y_train[i] == 0.0:
        target[i] = 'balanced'
    else:
        target[i] = 'unbalanced'
        







def SelectXY(Data, Mask, value):
    Selected = []
    for i in range(len(target)):
        if Mask[i] == value:
            Selected.append(Data[i,:])
    return np.array(Selected)

major_max = X_trans[:,0].max()
major_min = X_trans[:,0].min()
second_max = X_trans[:,1].max()
second_min = X_trans[:,1].min()
third_max = X_trans[:,2].max()
third_min = X_trans[:,2].min()

major_range = major_max - major_min
second_range = second_max - second_min
third_range = third_max - third_min

balanced_data = SelectXY(X_trans[:,0:3],target,'balanced')
unbalanced_data = SelectXY(X_trans[:,0:3],target,'unbalanced')








'''
Spec_figsize = (18, 12)
Spec_dpi = 80
plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)




import scipy.stats as stats
num_bins = 100

plt.subplot(231)
binwidth = (major_range+0.1*major_range) / num_bins
bins_major = np.arange(major_min-0.05*major_range, major_max+0.05*major_range + binwidth, binwidth)

dens_balanced = stats.gaussian_kde(balanced_data[:,0])
dens_unbalanced = stats.gaussian_kde(unbalanced_data[:,0])

plt.plot( bins_major, dens_balanced(bins_major))
plt.plot( bins_major, dens_unbalanced(bins_major))

plt.fill(bins_major, dens_balanced(bins_major), 'navy',
         bins_major, dens_unbalanced(bins_major), 'darkorange', alpha=0.3)

plt.xlim( major_min - 0.1 * major_range, major_max  + 0.1 * major_range)
plt.ylim( bottom = 1e-5)
plt.yscale("log")


plt.subplot(232)
binwidth = (second_range+0.1*second_range) / num_bins
bins_second = np.arange(second_min-0.05*second_range, second_max+0.05*second_range + binwidth, binwidth)

dens_balanced = stats.gaussian_kde(balanced_data[:,1])
dens_unbalanced = stats.gaussian_kde(unbalanced_data[:,1])

plt.plot( bins_second, dens_balanced(bins_second))
plt.plot( bins_second, dens_unbalanced(bins_second))

plt.fill(bins_second, dens_balanced(bins_second), 'navy',
         bins_second, dens_unbalanced(bins_second), 'darkorange', alpha=0.3)

plt.xlim( second_min - 0.1 * second_range, second_max  + 0.1 * second_range)
plt.ylim( bottom = 1e-5)
plt.yscale("log")


plt.subplot(233)
binwidth = (third_range+0.1*third_range) / num_bins
bins_third = np.arange(third_min-0.05*third_range, third_max+0.05*third_range + binwidth, binwidth)

dens_balanced = stats.gaussian_kde(balanced_data[:,2])
dens_unbalanced = stats.gaussian_kde(unbalanced_data[:,2])

plt.plot( bins_third, dens_balanced(bins_third))
plt.plot( bins_third, dens_unbalanced(bins_third))

plt.fill(bins_third, dens_balanced(bins_third), 'navy',
         bins_third, dens_unbalanced(bins_third), 'darkorange', alpha=0.3)

plt.xlim( third_min - 0.1 * third_range, third_max  + 0.1 * third_range)
plt.ylim( bottom = 1e-5)
plt.yscale("log")


plt.subplot(234)

plt.scatter(balanced_data[:,0], balanced_data[:,1], c='navy',s=0.5, cmap=plt.cm.coolwarm)
plt.scatter(unbalanced_data[:,0], unbalanced_data[:,1] , c='darkorange', s=0.5, cmap=plt.cm.coolwarm)

plt.xlabel('Major Component')
plt.ylabel('Second Component')

plt.xlim( major_min - 0.1 * major_range, major_max  + 0.1 * major_range)
plt.ylim( second_min- 0.1 *second_range, second_max + 0.1 * second_range)

plt.subplot(235)

plt.scatter(balanced_data[:,1], balanced_data[:,2], c='navy',s=0.5, cmap=plt.cm.coolwarm)
plt.scatter(unbalanced_data[:,1], unbalanced_data[:,2] , c='darkorange', s=0.5, cmap=plt.cm.coolwarm)

plt.xlabel('Second Component')
plt.ylabel('Third Component')

plt.xlim( second_min - 0.1 * second_range, second_max  + 0.1 * second_range)
plt.ylim( third_min- 0.1 *third_range, third_max + 0.1 * third_range)

plt.subplot(236)

plt.scatter(balanced_data[:,2], balanced_data[:,0], c='navy',s=0.5, cmap=plt.cm.coolwarm)
plt.scatter(unbalanced_data[:,2], unbalanced_data[:,0] , c='darkorange', s=0.5, cmap=plt.cm.coolwarm)

plt.xlabel('Third Component')
plt.ylabel('Major Component')

plt.xlim( third_min - 0.1 * third_range, third_max + 0.1 * third_range)
plt.ylim( major_min - 0.1 * major_range, major_max + 0.1 * major_range)
'''









#SVM

clf = SVC(kernel='linear', C=1.0)


clf.fit(X_train, Y_train)
summation = 0.
weight = np.zeros(26)
for j in range(26):
    weight[j] += clf.coef_[0,j]
    weight[j] /= np.std(X_train[:,j])
    summation += np.abs(weight[j])

for j in range(26):
    print('%.2f' % (weight[j]/summation*100.))

clf.fit(X_trans, Y_train)
summation = 0.
weight = np.zeros(26)
for j in range(26):
    for i in range(clf.coef_.shape[1]):
        weight[j] += clf.coef_[0,i] * pca.components_[i,j]
    weight[j] /= np.std(X_train[:,j])
    summation += np.abs(weight[j])

#print(clf.support_vectors_.shape, clf.support_vectors_[4][25])

print(weight/summation*100)


'''
true = 0
TP = 0
FP = 0
false = 0
TN = 0
FN = 0

for i in range(X_trans.shape[0]):
    predict = clf.coef_.dot(X_trans[i,:]) + clf.intercept_
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


'''
Spec_figsize = (12, 12)
Spec_dpi = 80
#plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)

fig = plt.figure(figsize=Spec_figsize, dpi=Spec_dpi)
ax = fig.add_subplot(111, projection='3d')

ax.scatter( balanced_data[:,0],
            balanced_data[:,1],
            balanced_data[:,2],
            label = 'Balanced',
            marker = 'o',
            c = 'navy')
ax.scatter( unbalanced_data[:,0],
            unbalanced_data[:,1],
            unbalanced_data[:,2],
            label = 'Unbalanced',
            marker = 'o',
            c = 'darkorange')


ax.scatter( clf.support_vectors_[:,0],
            clf.support_vectors_[:,1],
            clf.support_vectors_[:,2],
            label = 'Sopport Vectors',
            marker = '^',
            s = 100,
            c = 'green')


xlim = ax.get_xlim()
ylim = ax.get_ylim()
xx = np.linspace(-1100, -200, 30)
yy = np.linspace(ylim[0], ylim[1], 30)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T

Z = np.zeros(xy.shape[0])
#print(clf.intercept_);exit()
for i in range(Z.shape[0]):
    Z[i] = (-clf.intercept_[0] - clf.coef_[0,0] * xy[i,0] - clf.coef_[0,1] * xy[i,1]) / clf.coef_[0,2] 
Z = Z.reshape(XX.shape)
#print(Z);exit()
ax.plot_surface(XX,YY,Z,alpha=0.2,color='red')

ax.set_xlabel('Major Component')
ax.set_ylabel('Second Component')
ax.set_zlabel('third Component')
ax.legend(loc='upper right', shadow=True, fontsize='x-large')

plt.show()

'''








