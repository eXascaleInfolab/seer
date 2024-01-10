import sys
from subprocess import Popen, PIPE, STDOUT, DEVNULL # py3k

# setting path
sys.path.append('../../')
from systems.utils.library import *
from systems.utils import change_directory, parse_args, connection_class

import psycopg2

def get_connection(host="localhost", **kwargs):
    CONNECTION = f"postgres://postgres:postgres@{host}:5432/postgres"
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    def execute_query_f(sql):
        cursor.execute(sql)
        return cursor.fetchall()

    def write_query_f(sql):
        cursor.execute(sql)
        return conn.commit()


    conn_close_f = lambda : conn.close()
    return connection_class.Connection(conn_close_f, execute_query_f, write_query_f)


def parse_query(query ,*, date, rangeUnit , rangeL , sensor_list , station_list):
    temp = query.replace("<timestamp>", date)
    temp = temp.replace("<range>", str(rangeL))
    temp = temp.replace("<rangesUnit>", rangeUnit)

    # stations
    q = "(" + "'" + station_list[0] + "'"
    for j in station_list[1:]:
        q += ', ' + "'" + j + "'"
    q += ")"
    temp = temp.replace("<stid>", q)

    # sensors
    q = sensor_list[0]
    q_filter = '(' + sensor_list[0] + ' > 0.95'
    q_avg = 'avg(' + sensor_list[0] + ')'
    q_interpolate_avg = 'interpolate(avg(' + sensor_list[0] + '))'
    for j in sensor_list[1:]:
        q += ', ' + j
        # q_filter += ' OR ' + j + ' > 0.95'
        q_avg += ', ' + 'avg(' + j + ')'
        q_interpolate_avg += ', interpolate(avg(' + j + '))'

    temp = temp.replace("<sid>", q)
    temp = temp.replace("<sid1>", sensor_list[0] )
    sid2 = sensor_list[1] if len(sensor_list) > 1 else "s2"
    sid3 = sensor_list[2] if len(sensor_list) > 2 else "s3"
    temp = temp.replace("<sid2>", sid2)
    temp = temp.replace("<sid3>", sid3)
    temp = temp.replace("<interpolate_avg>", q_interpolate_avg)
    temp = temp.replace("<sfilter>", q_filter + ')')
    temp = temp.replace("<avg_s>", q_avg)

    return temp

def launch():
    
    print("launching timescaledb")

    with change_directory(__file__):
        process = Popen(['sh', 'variables.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()

        process = Popen(['sh', 'launch.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()

        process = Popen(['sleep', '10'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()

def stop():
   
    with change_directory(__file__):
        process = Popen(['sh', 'stop.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()


