#!/usr/bin/env python3

import psycopg2
import pg_conf
import numpy as np
import struct
import matplotlib.pyplot as plt
from pg_fetch import FetchNumberOfRow, FetchData, FetchLastTimeStamp, FetchData2, FetchLastTimeStamp2
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

index = []

XArray = []
YArray = []
ZArray = []

Theta = []
ReversedTheta = []
Phi = []

XYMag = np.zeros(100)
tan_theta = np.zeros(100)


plt.ion()

fig, axes = plt.subplots( nrows = 3, 
                          ncols = 2,
                          figsize = Spec_figsize, 
                          dpi = Spec_dpi
                          )
left_limit = -1500




axes[0,0].set( ylabel = 'Acceleration (mG)', title='Time series of X-axis' )
axes[0,0].set_xlim( left  = left_limit, right = 0.0)
lineX, = axes[0,0].plot([],[])

axes[1,0].set( ylabel = 'Acceleration (mG)', title='Time series of Y-axis' )
axes[1,0].set_xlim( left  = left_limit, right = 0.0)
lineY, = axes[1,0].plot([],[])

axes[2,0].set( xlabel = 'Record Number', ylabel = 'Acceleration (mG)', title='Time series of Z-axis' )
axes[2,0].set_xlim( left  = left_limit, right = 0.0)
lineZ, = axes[2,0].plot([],[])

axes[1,1].set( ylabel = 'Theta (rad)', title='Time series of Theta' )
axes[1,1].set_xlim( left  = left_limit, right = 0.0)
axes[1,1].set_ylim( top  = np.pi, bottom = 0.0)
lineTheta, = axes[1,1].plot([],[], color='c')

axes[2,1].set( xlabel = 'Record Number', ylabel = 'Phi (rad)', title='Time series of Phi' )
axes[2,1].set_xlim( left  = left_limit, right = 0.0)
axes[2,1].set_ylim( top  = 2. * np.pi, bottom = 0.0)
linePhi, = axes[2,1].plot([],[], color='m')


ax_polar = plt.subplot(322, polar=True)
ax_polar.set_rmax(0.5 * np.pi)
ax_polar.set_rmin(0.0)
ax_polar.grid(True)
ax_polar.set_title("Orientation", va='bottom')
linePolar, = ax_polar.plot([], [], color='r', linewidth=3, marker=".")
linePolar_ReversedTheta, = ax_polar.plot([], [], color='g', linewidth=3, marker=".")



LastTimeStamp = FetchLastTimeStamp(cur)

while True:
    
    NewTimeStamp = FetchLastTimeStamp(cur)

    if NewTimeStamp > LastTimeStamp:

        data = FetchData( cur, NewTimeStamp, LastTimeStamp)
            
        for row in range(-1,-len(data)-1,-1):
        
            time    = data[row][0]
            length  = data[row][1]
            payload = data[row][2]
            
            if len(payload) == length == 1200:
                TimeStamp.append(time)
                RAW_DATA = np.array( list( struct.unpack( 'f'*300, payload ) ) )
                
                Nvalue = len(RAW_DATA)
                Ndata = int(Nvalue/3)
                RAW_DATA = RAW_DATA.reshape( (Ndata, 3))
                
                
                for i in range(Ndata):
                    XYMag[i] = np.linalg.norm(RAW_DATA[i,0:2])


                RAW_DATA = RAW_DATA.T
                XArray = np.concatenate( (XArray, RAW_DATA[0,:]), axis=0)
                YArray = np.concatenate( (YArray, RAW_DATA[1,:]), axis=0)
                ZArray = np.concatenate( (ZArray, RAW_DATA[2,:]), axis=0)
                
                ThetaData = np.arctan2(XYMag, RAW_DATA[2,:])
                Theta = np.concatenate( (Theta, ThetaData), axis=0)
                
                ReversedThetaData = np.pi - ThetaData
                for i in range(len(ThetaData)):
                    if ThetaData[i] > 0.5*np.pi:
                        ThetaData[i] = np.nan
                    if ReversedThetaData[i] > 0.5*np.pi:
                        ReversedThetaData[i] = np.nan
                
                PhiData = np.arctan2(RAW_DATA[1,:],RAW_DATA[0,:]) + np.pi
                Phi = np.concatenate( (Phi, PhiData), axis=0)
                
                
                    
                
                if len(XArray) > np.abs(left_limit):
                    XArray = XArray[left_limit:-1]
                    YArray = YArray[left_limit:-1]
                    ZArray = ZArray[left_limit:-1]
                    
                    Theta = Theta[left_limit:-1]
                    Phi = Phi[left_limit:-1]


                index = range(-len(XArray),0)
                
                lineX.set_xdata(index)
                lineX.set_ydata(XArray)
                
                lineY.set_xdata(index)
                lineY.set_ydata(YArray)
                
                lineZ.set_xdata(index)
                lineZ.set_ydata(ZArray)
                
                linePolar.set_data(PhiData, ThetaData)
                linePolar_ReversedTheta.set_data(PhiData, ReversedThetaData)
                
                lineTheta.set_xdata(index)
                lineTheta.set_ydata(Theta)
                
                linePhi.set_xdata(index)
                linePhi.set_ydata(Phi)
                
                #Need both of these in order to rescale
                axes[0,0].relim()
                axes[0,0].autoscale_view()
                axes[1,0].relim()
                axes[1,0].autoscale_view()
                axes[2,0].relim()
                axes[2,0].autoscale_view()

                
                #We need to draw *and* flush
                fig.canvas.draw()
                fig.canvas.flush_events()
                
            elif len(payload) == length:
                print('Drop out the data at row', iROW+1,', length =',length)
            else:
                print('data loss at ', time)
        
        LastTimeStamp = NewTimeStamp
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
