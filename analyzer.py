#!/usr/bin/env python
__author__      = "I-Ta Hsieh"
__copyright__   = "Private use"

# The data path
DataFile = './data/fea1_0409.bin'

from DataIO import ImportData, ColumnDict
Array = ImportData(DataFile)

import numpy as np
Array = np.array(Array)

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(16, 12), dpi=80)
ax.plot(Array[:,ColumnDict["Xmean"]])
ax.set(xlabel='time (s)', ylabel='Mean',
       title='About as simple as it gets, folks')
ax.grid()

ImageFileName = "test.png"
fig.savefig(ImageFileName)
#plt.show()
