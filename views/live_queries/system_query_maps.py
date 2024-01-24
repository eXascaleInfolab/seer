import random
import time
from collections import namedtuple

import numpy as np

from utils.query_translator import load_query
import os
from systems import clickhouse, timescaledb, influx, monetdb

# host differ whetever using docker and if using docker the host is the name of the container or path to the host of the docker
hosts = {"clickhouse": "clickhouse" if os.getenv("using_docker") else "localhost",
         "timescaledb": "timescaledb" if os.getenv("using_docker") else "localhost",
         "influx": os.getenv("DOCKER_HOST", "localhost"),
         "monetdb": os.getenv("DOCKER_HOST", "localhost"),
         }

system_module_map = {"clickhouse": clickhouse,
                 "timescaledb": timescaledb,
                 "influx": influx,
                 "monetdb": monetdb,
                 }


def run_query(system, q_n, rangeL, rangeUnit, n_st, n_s, n_it=1, dataset="d1"):
    print("running query", q_n, "on system", system)
    query_template = load_query(system, q_n)
    query_template = query_template.replace("<db>", "d1")

    system_module = system_module_map[system]

    host = hosts[system]
    system_connection = system_module.get_connection(host=host, dataset=dataset)

    date = "2019-04-01T00:00:00"
    random_stations = ['st' + str(z) for z in random.sample(range(10), n_st)]
    random_sensors = ['s' + str(z) for z in random.sample(range(100), n_s)]

    parsed_query = system_module.parse_query(query_template, date=date, rangeUnit=rangeUnit, rangeL=rangeL,
                                             sensor_list=random_sensors, station_list=random_stations)
    runtimes = []
    try:
        for i in range(n_it+2):# 2 warmup queries
            start = time.time()
            query_data = system_connection.execute(parsed_query)
            runtime = (time.time() - start) * 1000
            if i > 1:
                runtimes.append(runtime)
        # print(query_data)
    except Exception as e:
        print(e)
        print("error in query;", parsed_query)
        query_data = []

    runtime = np.mean(runtimes)

    runtime = round(runtime, 2)
    print(query_data)
    if system == "influx":
        query_data = [ list(result) for result in  query_data][0]
        #cast dict to tuples (key1,value1,key2 ,value2..
        query_data = [tuple(result.items())[:]   for result in  query_data]

    query_data = sorted(query_data, key=lambda x: x[0])


    QueryResult = namedtuple("QueryResult", "runtime query_data query runtimes")
    print("W")
    return QueryResult(runtime, query_data, parsed_query , runtimes)
