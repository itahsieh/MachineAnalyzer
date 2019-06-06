import numpy as np

def FetchNumberOfRow(cursor):
    cursor.execute(
        "SELECT count(*) FROM raw" 
        )
    return cursor.fetchall()[0][0]


def FetchData(cursor, LaterTimestamp, EarlyTimestamp):
    cursor.execute(
        "SELECT captured, data_len, data FROM raw " +
        "WHERE captured <= '"+str(LaterTimestamp)+"' and captured > '"+str(EarlyTimestamp)+"' "
        "ORDER BY captured DESC " 
        )
    return np.array(cursor.fetchall())

def FetchLastTimestamp(cursor):
    cursor.execute(
        "SELECT captured FROM raw "
        "ORDER BY captured DESC " +
        "LIMIT 1"
        )
    return cursor.fetchall()[0][0]
