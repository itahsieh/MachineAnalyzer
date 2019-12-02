import sys
import serial
import time
from MA_utilities import *

class sensor():
    def __init__(self, ser_port, print_out):
        if print_out:
            print( bcolors.WARNING +
               'LIST the configuration of the sensor' +
               bcolors.ENDC )
        
        SendCommand( ser_port, 'LIST')
        while ser_port.inWaiting() > 0:
            response = ser_port.readlines()
            for i in range(len(response)): 
                line = response[i].strip().decode('charmap')
                if print_out:
                    print(line)
                
                # attributes of firmware 
                if 'FIRMWARE VERSION' in line:
                    self.version = line.split(":",1)[1].replace(" ", "")
                elif 'BUILD DATE' in line:
                    self.version = line.split(":",1)[1].split()
                # attributes of sensor
                elif 'SENSOR ID' in line:
                    self.ID = line.split(":",1)[1].replace(" ", "")
                elif 'SENSOR Output Data Type' in line:
                    self.output = line.split(":",1)[1].split()
                elif 'Output Checksum Type' in line:
                    self.checksum_type = line.split(":",1)[1].replace(" ", "")
                elif 'SENSOR Sampling Rate' in line:
                    self.SamplingRate = line.split(":",1)[1].split()
                elif 'RAW DATA OUT AXIS' in line:
                    self.raw_axis = line.split(":",1)[1].replace(" ", "")


def SerialConnect( Port, BaudRate):
    try:
        ser = serial.Serial(
            port = Port, 
            baudrate = BaudRate, 
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            timeout = 1
            )
        return ser
    except:
        sys.exit("Error connecting device")


def SendCommand( ser_port, string):
    AT_string = 'AT$' + string + '\r'
    ser_port.write(AT_string.encode() )
    ser_port.flush()
    time.sleep(0.1)

    
def ListConfig(ser_port):
    sensor_config = sensor( ser_port, print_out = True) 
    return sensor_config

