#!/usr/bin/env python3

import psycopg2
import pg_conf
import numpy as np
import struct
import matplotlib.pyplot as plt
from pg_fetch import FetchNumberOfRow, FetchData, FetchLastTimestamp
import time as PyTime

Spec_figsize = (16, 12)
Spec_dpi = 80


conn = psycopg2.connect(
    database    = pg_conf.database, 
    user        = pg_conf.user, 
    password    = pg_conf.password, 
    host        = pg_conf.host,
    port        = pg_conf.port,
    )
print("Opened database successfully")

cur = conn.cursor()

#select data


TimeStamp =[]
XArray = []
YArray = []
ZArray = []
index = []



plt.ion()

fig, axes = plt.subplots( nrows = 3, 
                          ncols = 1,
                          figsize = Spec_figsize, 
                          dpi = Spec_dpi
                          )
left_limit = -1500




axes[0].set( ylabel = 'Acceleration (mG)', title='Time series of X-axis' )
axes[0].set_xlim( left  = left_limit, right = 0.0)
lineX, = axes[0].plot([],[])

axes[1].set( ylabel = 'Acceleration (mG)', title='Time series of Y-axis' )
axes[1].set_xlim( left  = left_limit, right = 0.0)
lineY, = axes[1].plot([],[])

axes[2].set( xlabel = 'Record Number', ylabel = 'Acceleration (mG)', title='Time series of Z-axis' )
axes[2].set_xlim( left  = left_limit, right = 0.0)
lineZ, = axes[2].plot([],[])

LastTimestamp = FetchLastTimestamp(cur)

while True:
    
    LastTimestamp_new = FetchLastTimestamp(cur)
    
    #if (LastTimestamp_new - LastTimestamp).seconds > 1.0:
        #print('Has to update more than one timestamp')
    
    if LastTimestamp_new > LastTimestamp:

        data = FetchData( cur, LastTimestamp_new, LastTimestamp)
            
        for row in range(-1,-len(data)-1,-1):
        
            time    = data[row][0]
            length  = data[row][1]
            payload = data[row][2]
            
            if len(payload) == length == 1200:
                TimeStamp.append(time)
                RAW_DATA = np.array( list( struct.unpack( 'f'*300, payload ) ) )
                Nvalue = len(RAW_DATA)
                RAW_DATA = RAW_DATA.reshape((int(Nvalue/3),3)).T
                
                XArray = np.concatenate( (XArray, RAW_DATA[0,:]), axis=0)
                YArray = np.concatenate( (YArray, RAW_DATA[1,:]), axis=0)
                ZArray = np.concatenate( (ZArray, RAW_DATA[2,:]), axis=0)
                
                if len(XArray) > np.abs(left_limit):
                    XArray = XArray[left_limit:-1]
                    YArray = YArray[left_limit:-1]
                    ZArray = ZArray[left_limit:-1]


                index = range(-len(XArray),0)
                
                lineX.set_xdata(index)
                lineX.set_ydata(XArray)
                
                lineY.set_xdata(index)
                lineY.set_ydata(YArray)
                
                lineZ.set_xdata(index)
                lineZ.set_ydata(ZArray)
                
                #Need both of these in order to rescale
                axes[0].relim()
                axes[0].autoscale_view()
                axes[1].relim()
                axes[1].autoscale_view()
                axes[2].relim()
                axes[2].autoscale_view()
                
                #We need to draw *and* flush
                fig.canvas.draw()
                fig.canvas.flush_events()
                
            elif len(payload) == length:
                print('Drop out the data at row',iROW+1,', length =',length)
            else:
                print('data loss at ',time)
        
        LastTimestamp = LastTimestamp_new
    PyTime.sleep(0.5)



'''
TimeStamp =[]
Array = []
for iROW in range(len(dataset)):
    time    = dataset[iROW][1]
    length  = dataset[iROW][2]
    payload = dataset[iROW][3]
    if len(payload) == length == 1200:
        data = struct.unpack( 'f'*300, payload )
        Array.extend(list(data))
        TimeStamp.append(time)
    elif len(payload) == length:
        print('Drop out the data at row',iROW+1,', length =',length)
    else:
        print('data loss at ',time)

Array = np.array(Array)
Nvalue = len(Array)
print(Nvalue)
Array = Array.reshape((int(Nvalue/3),3)).T

DataType = 'X-axis'
Spec_figsize = (16, 12)
Spec_dpi = 80
fig, axes = plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)
axes.plot(Array[0,:])
axes.set( xlabel = 'Time', ylabel = DataType, title='Time series of ' + DataType)
plt.show()
'''
