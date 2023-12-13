import random
import json
from utils.time_utils import random_date

set_st = [str(random.randint(0, 9)) for i in range(500)]
set_s = [str(random.randint(0, 99)) for i in range(500)]
set_date = [random.random() for i in range(500)]


def load_query(system,q):
    path = f"systems/{system}/queries.sql"
    with open(path) as file:
        queries = [line.rstrip() for line in file]
    return queries[int(q[-1])-1]

def clickhouse_query_parser(query ,*,  date, rangeUnit , rangeL , sensor_list , station_list):
    query = query.replace("<timestamp>", date)
    query = query.replace("<range>", str(rangeL))
    query = query.replace("<rangesUnit>", rangeUnit)

    # sensors
    q = sensor_list[0]
    q_filter = '(' + sensor_list[0] + ' > 0.95' + ')'
    q_avg = 'avg(' + sensor_list[0] + ')'
    for j in sensor_list[1:]:
        q += ', ' + j
        q_avg += ', ' + 'avg(' + j + ')'

    query = query.replace("<sid>", q)
    query = query.replace("<sfilter>", q_filter)
    query = query.replace("<avg_s>", q_avg)
    query = query.replace("<sid1>", "1")
    query = query.replace("<sid2>", "2")

    if "fill step" in query.lower():
        if len(station_list) == 1:
            q = "('" + 'st' + str(random.sample(range(10), 1)[0]) + "')"
            query = query.replace("<stid>", q)

        else:
            fill_commands = []  # queries to unite
            for station in station_list:
                q = f"('{station}')"
                station_fill = query.replace("<stid>", q).replace(";", "")
                fill_commands.append(station_fill)

            query = "SELECT * FROM (" + " UNION ALL ".join(fill_commands) + ")"

    else:  # normal station insertion
        q = "(" + ', '.join(["'" + j + "'" for j in station_list]) + ")"
        query = query.replace("<stid>", q)

    return query


def timescaledb_query_parser(query ,*, date, rangeUnit , rangeL , sensor_list , station_list):
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