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

def FetchLastTimeStamp(cursor):
    cursor.execute(
        "SELECT captured FROM raw "
        "ORDER BY captured DESC " +
        "LIMIT 1"
        )
    return cursor.fetchall()[0][0]

def FetchLastTimeStamp2(cursor):
    cursor.execute(
        "SELECT captured FROM raw "
        "ORDER BY received DESC " +
        "LIMIT 1"
        )
    return cursor.fetchall()[0][0]

def FetchLastRecord(cursor, n):
    cursor.execute(
        "SELECT captured FROM raw "
        "ORDER BY received DESC " +
        "LIMIT " + str(n)
        )
    return cursor.fetchall()


def FetchData2(cursor, LaterTimestamp, EarlyTimestamp):
    cursor.execute(
        "SELECT received, data_len, data FROM raw " +
        "WHERE received <= '"+str(LaterTimestamp)+"' and received > '"+str(EarlyTimestamp)+"' "
        "ORDER BY received DESC " 
        )
    return np.array(cursor.fetchall())
