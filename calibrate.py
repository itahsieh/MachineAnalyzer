#!/usr/bin/env python3
# prerequisite: pip3 install pyserial

import serial
from ast import literal_eval
import threading
import struct
import time
import sys
#import matplotlib.pyplot as plt

#Spec_figsize = (16, 12)
#Spec_dpi = 80

buffer_size = 1400
AverageInterval = 1.



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def SendCommand( ser_port, string):
    AT_string = 'AT$' + string + '\r'
    ser_port.write(AT_string.encode() )
    time.sleep(0.1)
    ser_port.flush()
    
def ListConfig(ser_port):
    SendCommand( ser, 'LIST')
    while ser.inWaiting() > 0:
        response = ser.readlines()
        print(
            bcolors.WARNING +
            'LIST the configuration of the sensor' +
            bcolors.ENDC
            )
        for i in range(len(response)):
            line = response[i].strip().decode('charmap')
            print(repr(line).strip('"\''))

def RawAverage(ser_port):   
    

    #binary_file = open("test.dat", 'wb')
    count = 0
    Xmean = 0.
    Ymean = 0.
    Zmean = 0.
    
    Zarray = []
    
    
    ser_port.flushInput()
    ser_port.flushOutput()
    ser_port.read(1200)

    T_start = time.time()
    while True:
        buffer = ser_port.read(buffer_size)
        raw_list = buffer.split(b'\xa5')
        
        for i in range(1,len(raw_list)-1):
            #print(len(raw_list[i]))
            if len(raw_list[i]) == 13:
                
                #binary_file.write(raw_list[i][0:12])
                
                raw_float = struct.unpack( 'f'*3, raw_list[i][0:12] ) 
                
                # print float as screen output
                #print(raw_float)
                
                Xmean += raw_float[0]
                Ymean += raw_float[1]
                Zmean += raw_float[2]
                
                count += 1
                
                Zarray.append(raw_float[2])
        
        if (time.time() - T_start) > AverageInterval:
            break

    Xmean /= float(count)
    Ymean /= float(count)
    Zmean /= float(count)

    print('Means of X, Y, Z:', Xmean, Ymean, Zmean)
    
    #fig, axes = plt.subplots(figsize=Spec_figsize, dpi=Spec_dpi)
    #axes.plot(Zarray)
    #axes.set(xlabel='Record number', ylabel = 'acceleration',
            #title='Time series of Z-acceleration')
    #axes.grid(True)

    #binary_file.close()
    return Xmean, Ymean, Zmean



try:
    ser = serial.Serial(
        port = "/dev/ttyUSB0", 
        baudrate = 19200, 
        bytesize = serial.EIGHTBITS,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        timeout = 1
        )
except:
    sys.exit("Error connecting device")


#ListConfig(ser)

SendCommand( ser, 'RAW')
SendCommand( ser, 'RS')

input( bcolors.HEADER +
    'Place first position:\n' + 
    str(AverageInterval) + ' secs to clculate average\n' + 
    bcolors.ENDC +
    "Press Enter to continue...")
X1, Y1, Z1 = RawAverage(ser)

input( bcolors.HEADER +
    'Reverse along X-axis:\n' + 
    str(AverageInterval) + ' secs to clculate average\n' +
    bcolors.ENDC +
    "Press Enter to continue...")
X2, Y2, Z2 = RawAverage(ser)

input( bcolors.HEADER +
    'Reverse along Y-axis:\n' + 
    str(AverageInterval) + ' secs to clculate average\n' +
    bcolors.ENDC +
    "Press Enter to continue...")
X3, Y3, Z3 = RawAverage(ser)

print('X-bias:', 0.5*(0.5*(X1+X2) + X3))
print('Y-bias:', 0.5*(0.5*(Y2+Y3) + Y1))
print('Z-bias:', 0.5*(0.5*(Z1+Z3) + Z2))

ser.close()
#plt.show()


