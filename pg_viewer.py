#!/usr/bin/env python3

import psycopg2
import numpy as np
import struct

conn = psycopg2.connect(
    database    = "accelerometer", 
    user        = "postgres", 
    password    = "postgres", 
    host        = "220.135.143.199", 
    port        = "5432"
    )
print("Opened database successfully")


#select data
cur = conn.cursor()
cur.execute(
    "SELECT source,received,length,payload FROM raw" 
    )
dataset = cur.fetchall()
dataset = np.array(dataset)


Array = []
for iROW in range(len(dataset)):
    time    = dataset[iROW][1]
    length  = dataset[iROW][2]
    payload = dataset[iROW][3]
    if len(payload) == length:
        print('length compatable',len(payload),length)
        data = struct.unpack( 'f'*300, payload )
        Array.append(list(data))
    else:
        print('data loss at ',time)
print(data)
