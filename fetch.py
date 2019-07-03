#!/usr/bin/env python3
# prerequisite: pip3 install pyserial

import serial
from ast import literal_eval
import struct
import time

buffer_size = 1400

binary_file = open("test.dat", 'wb')

ser = serial.Serial(
    port = "/dev/ttyUSB0", 
    baudrate = 19200, 
    bytesize = serial.EIGHTBITS,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    timeout= 1,
    )
ser.flush() 
assert ser.isOpen()


ser.write(b'AT$S')
ser.write(b'AT$RAW')
ser.write(b'AT$RS')

T_start = time.time()
while True:
    buffer = ser.read(buffer_size)
    raw_list = buffer.split(b'\xa5')
    
    for i in range(1,len(raw_list)-1):
        #print(len(raw_list[i]))
        if len(raw_list[i]) == 13:
            binary_file.write(raw_list[i][0:12])
            
            #raw_float = struct.unpack( 'f'*3, raw_list[i][0:12] )
            
            # print float as screen output
            #print(raw_float)
    
    T_temp = time.time()
    if (T_temp - T_start) > 5.:
        break
    
binary_file.close()

ser.close()


