#!/usr/bin/env python3

#from sklearn.svm import SVC
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
