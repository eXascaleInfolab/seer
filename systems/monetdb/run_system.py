import sys
import pandas as pd
import json

from subprocess import Popen, PIPE, STDOUT, DEVNULL  # py3k

# setting path
sys.path.append('../../')
from systems.utils.library import *
from systems.utils import change_directory, parse_args, connection_class

import pymonetdb

def get_connection(host="localhost", **kwargs):
    conn = pymonetdb.connect(username="monetdb", port=54320, password="monetdb", hostname=host, database="mydb")
    cursor = conn.cursor()
    # isolation_level = "SERIALIZABLE"  # For the online queries
    # cursor.execute(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}")

    def execute_query_f(sql):
        cursor.execute(sql)
        return cursor.fetchall()

    def write_query_f(sql):
        lines = cursor.execute(sql)
        cursor.commit()
        return lines

    conn_close_f = lambda : conn.close()
    return connection_class.Connection(conn_close_f, execute_query_f,write_query_f)


def parse_query(query, *, date, rangeUnit, rangeL, sensor_list, station_list):
    if rangeUnit in ["week", "w", "WEEK"]:
        rangeUnit = "day"
        rangeL = rangeL * 7

    temp = query.replace("<timestamp>", date)
    temp = temp.replace("<range>", str(rangeL))
    temp = temp.replace("<rangesUnit>", rangeUnit)

    # stations
    q = "(" + "'" + station_list[0] + "'"
    for j in station_list[1:]:
        q += ', ' + "'" + j + "'"
    q += ")"

    temp = temp.replace("<stid>", q)
    stid1 = station_list[0]
    stid2 = "" + station_list[1] + "" if len(station_list) > 1 else "st0"
    temp = temp.replace("<stid1>", stid1)
    temp = temp.replace("<stid2>", stid2)

    # sensors
    q = sensor_list[0]
    q_filter = '(' + sensor_list[0] + ' > 0.95'
    q_avg = 'avg(' + sensor_list[0] + ')'
    for j in sensor_list[1:]:
        q += ', ' + j
        # q_filter += ' OR ' + j + ' > 0.95'
        q_avg += ', ' + 'avg(' + j + ')'

    temp = temp.replace("<sid>", q)
    sid1 = sensor_list[0]
    sid2 = sensor_list[1] if len(sensor_list) > 1 else "s2"
    sid3 = sensor_list[2] if len(sensor_list) > 3 else "s3"
    temp = temp.replace("<sid1>", sid1)
    temp = temp.replace("<sid2>", sid2)
    temp = temp.replace("<sid3>", sid3)
    temp = temp.replace("<sfilter>", q_filter + ')')
    temp = temp.replace("<avg_s>", q_avg)

    import re
    # match a=(b,c,...) make it a=b or a=c or ...
    equality_missmatches = re.findall(r"\b\w+\s*=\s*\([^)]*?,[^)]*?\)", temp)
    for equality_missmatch in equality_missmatches:
        pattern, options = equality_missmatch.split("=")
        options = options.replace(")", "").replace("(", "").split(",")
        res = "(" + " or ".join([pattern + "= " + o for o in options]) + ")"
        temp = temp.replace(equality_missmatch, res)

    return temp
