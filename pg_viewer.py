#!/usr/bin/env python3

import psycopg2
import pg_conf
import numpy as np
import struct

conn = psycopg2.connect(
    database    = pg_conf.database, 
    user        = pg_conf.user, 
    password    = pg_conf.password, 
    host        = pg_conf.host,
    port        = pg_conf.port,
    )
print("Opened database successfully")


#select data
cur = conn.cursor()
cur.execute(
    "SELECT source,received,length,payload FROM raw" 
    )
dataset = cur.fetchall()
dataset = np.array(dataset)
print('number of data row:',len(dataset))

TimeStamp =[]
Array = []
for iROW in range(len(dataset)):
    time    = dataset[iROW][1]
    length  = dataset[iROW][2]
    payload = dataset[iROW][3]
    if len(payload) == length == 1200:
        data = struct.unpack( 'f'*300, payload )
        Array.append(list(data))
        TimeStamp.append(time)
    elif len(payload) == length:
        print('length',length,'at row',iROW+1)
    else:
        print('data loss at ',time)
