import os
import struct

# single-precision data format --> DataType_Nbyte = 4 bytes
DataType_Nbyte = 4

# The order of the data format
FEA_ColumnDict = {
    "Xmean"     : 0,
    "Xstd"      : 1,
    "Xrms"      : 2, 
    "Xcrest"    : 3,
    "Xskewness" : 4,
    "Xkurtosis" : 5,
    "Xmax"      : 6,
    "Xvel"      : 7,
    
    "Ymean"     : 8,
    "Ystd"      : 9,
    "Yrms"      : 10, 
    "Ycrest"    : 11,
    "Yskewness" : 12,
    "Ykurtosis" : 13,
    "Ymax"      : 14,
    "Yvel"      : 15, 
    
    "Zmean"     : 16,
    "Zstd"      : 17,
    "Zrms"      : 18,  
    "Zcrest"    : 19,
    "Zskewness" : 20,
    "Zkurtosis" : 21,
    "Zmax"      : 22,
    "Zvel"      : 23,
    
    "Temprature": 24,
    "SensorTemprature": 25
    }
# number of columns for single row data
Ncolumn = len(FEA_ColumnDict)

def ImportFeaData(DataPath):
    # calculate data size and number of rows
    DataSize = os.stat(DataPath).st_size
    Nrow = int( DataSize / DataType_Nbyte / Ncolumn ) 

    Array = []
    with open(DataPath, "rb") as f:
        for i in range(Nrow):
            row = struct.unpack( 'f'*Ncolumn, f.read( DataType_Nbyte * Ncolumn ) )
            Array.append(list(row))
    
    return Array

def ImportRawData(DataPath):
    DataSize = os.stat(DataPath).st_size
    Nvalue = int( DataSize / DataType_Nbyte ) 
    
    with open(DataPath, "rb") as f:
        Array = struct.unpack( 'f'*Nvalue, f.read( DataType_Nbyte * Nvalue ) )
    
    return list(Array)
    
def DataImport(opt):
    # Data IO
    # try if the file exists
    try:
        fh = open(opt.DataPath, 'r')
        fh.close()
    except FileNotFoundError:
        print('Data not found:',opt.DataPath)
        exit(1)
    # DataType: 'feature', 'raw', or 'fft'
    if 'fea' in opt.filename or opt.fea_data:
        opt.DataType = 'feature'
        Array = ImportFeaData(opt.DataPath)
    elif 'raw' in opt.filename or opt.raw_data or opt._3ax_raw_data:
        opt.DataType = 'raw'
        Array = ImportRawData(opt.DataPath)
    elif 'fft' in opt.filename:
        opt.DataType = 'fft' 
        pass
    else:
        print('Could not identify the data type')
        exit(1)
    
    # convert the array to numpy type
    import numpy as np
    Array = np.array(Array)
    if opt._3ax_raw_data:
        Nvalue = len(Array)
        Array = Array.reshape((int(Nvalue/3),3)).T
        if opt.axis == 'x':
            Array = Array[0,:]
        elif opt.axis == 'y':
            Array = Array[1,:]
        elif opt.axis == 'z':
            Array = Array[2,:]
    
    return Array
    
    
    



