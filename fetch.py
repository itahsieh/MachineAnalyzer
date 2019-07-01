# pip3 install pyserial
import serial
from ast import literal_eval
import struct


buffer_size = 1400

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

while True:
    s = ser.read(buffer_size)
    raw_list = s.split(b'\xa5')
    
    print(len(raw_list))
    
    for i in range(1,len(raw_list)-1):
        #print(len(raw_list[i]))
        if len(raw_list[i]) == 13:
            raw_float = struct.unpack( 'f'*3, raw_list[i][0:12] )

            print(raw_float)

ser.close()


