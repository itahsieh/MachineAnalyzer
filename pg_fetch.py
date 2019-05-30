import numpy as np

def FetchNumberOfRow(cursor):
    cursor.execute(
        "SELECT count(*) FROM raw" 
        )
    return cursor.fetchall()[0][0]


def FetchData(cursor, NumberOfLast):
    cursor.execute(
        "SELECT received,length,payload FROM raw " +
        "ORDER BY received DESC " +
        "LIMIT " + str(NumberOfLast)
        )
    return np.array(cursor.fetchall())
