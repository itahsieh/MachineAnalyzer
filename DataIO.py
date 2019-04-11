# single-precision data format --> DataType_Nbyte =4 bytes
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

def ImportData( DataType, DataPath):
    # calculate data size and number of rows
    import os
    DataSize = os.stat(DataPath).st_size
    Nrow = int( DataSize / DataType_Nbyte / Ncolumn ) 

    import struct
    Array = []
    with open(DataPath, "rb") as f:
        for i in range(Nrow):
            row = struct.unpack( 'f'*Ncolumn, f.read( DataType_Nbyte * Ncolumn ) )
            Array.append(list(row))
    
    return Array





