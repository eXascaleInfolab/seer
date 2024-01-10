import sys


# setting path
sys.path.append('../../')
sys.path.append("systems")

from systems.utils.library import *

from systems.utils import change_directory , parse_args , connection_class

from influxdb import InfluxDBClient
from subprocess import Popen, PIPE, STDOUT, DEVNULL # py3k



def get_connection(host="localhost", dataset=None , **kwargs):
    client = InfluxDBClient(host=host, port=8086, username='name')

    def execute_query_f(sql):
        return client.query(sql)

    def write_points_f(points ,dataset=dataset):
        #input: "sensor,id_station=st99 s0=<>,s1=0.256154,s2=0.353368,s3=0.264800,s4=0.340716 ....

        assert dataset is not None, "influx requires the dataset to be specified"
        return client.write_points(points, database=dataset, time_precision="ms", batch_size=5000 ,protocol='line')

    conn_close_f = lambda : client.close()
    return connection_class.Connection(conn_close_f, execute_query_f, write_points_f)


def parse_query(query ,*, date, rangeUnit , rangeL , sensor_list , station_list):
    temp = query.replace("<timestamp>", date)
    if rangeUnit == "month":
        rangeL = rangeL * 30
        rangeUnit = "day"

    temp = temp.replace("<range>", str(rangeL))
    temp = temp.replace("<rangesUnit>", str(rangeUnit[0]))
    # stations

    q = '(id_station =' + "'" + station_list[0] + "'"
    for j in station_list[1:]:
        q += ' OR ' + 'id_station =' + "'" + j + "'"
    q += ")"
    temp = temp.replace("<stid>", q)

    # sensors
    q = ",".join(sensor_list)
    q_filter = "( " + sensor_list[0] + ' > 0.95' + ")"
    q_avg = ",".join([f"mean({e})" for e in sensor_list])  # 'mean(' + li[0] + ')'
    q_avg_ = ",".join([f"mean_{e}" for e in sensor_list])
    q_avg_as = ",".join([f"mean({e})  as mean_{e}" for e in sensor_list])

    temp = temp.replace("<sid>", q)
    temp = temp.replace("<sid1>", "s1")
    temp = temp.replace("<sid2>", "s2")
    temp = temp.replace("<sid>", q)
    temp = temp.replace("<sfilter>", q_filter)
    temp = temp.replace("<avg_s>", q_avg)
    temp = temp.replace("<avg_s_>", q_avg_)
    temp = temp.replace("<avg_s_as>", q_avg_as)

    return temp


def launch():
    print("launching influx")
    
    with change_directory(__file__):
        main_process = Popen(['sh', 'launch.sh' ], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        process = Popen(['sleep', '20'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()

def stop():
    print("shutting down")
    command = "ps -ef | grep 'influxd' | grep -v grep | awk '{print $2}' | xargs -r kill -9"
    process = Popen(command, shell=True, stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    stdout, stderr = process.communicate()
    
    

