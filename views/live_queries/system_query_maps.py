"""
    This file contains the functions to run a query on a system.
    
    The host of the system is defined in the hosts dict. Depending if the tool is run using docker or with the basic
    django command python3 manage.py runserver to test it locally the host for the system differ.
    In the docker compose file we set a environment variable "using_docker" to true that can be used to know if the code
    is run with docker or not. We additionally set the variable DOCKER_HOST in the docker-compose file
    to obtain the host of the docker container.
    If you run the systems on a different host/server you need to change the host in the host dict.
    Consider how to set the host from within the docker container since docker has its own network.
"""

import random
import time
from collections import namedtuple
import numpy as np
from utils.query_translator import load_query
import os
from systems import clickhouse, timescaledb, influx, monetdb, mongodb

hosts = {"clickhouse": "clickhouse" if os.getenv("using_docker") else "localhost",
         "timescaledb": "timescaledb" if os.getenv("using_docker") else "localhost",
         "influx": "localhost",
         "monetdb": os.getenv("DOCKER_HOST", "localhost"),
         "mongodb": os.getenv("DOCKER_HOST", "localhost"),
         }

system_module_map = {"clickhouse": clickhouse,
                     "timescaledb": timescaledb,
                     "influx": influx,
                     "monetdb": monetdb,
                     "mongodb": mongodb,
                     }


def run_query(system, q_n, rangeL, rangeUnit, n_st, n_s, n_it=1, dataset="d1"):
    print("running query\n", q_n, rangeL, rangeUnit, n_st, n_s, "on system", system)
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
    print(parsed_query)
    runtimes = []
    try:
        for i in range(n_it + 2):  # 2 warmup queries
            print("iteration:", i)
            start = time.time()
            query_data = system_connection.execute(parsed_query)
            runtime = (time.time() - start) * 1000
            if i > 1:
                runtimes.append(runtime)

    except Exception as e:
        print(e)
        print("error in query;", parsed_query)
        query_data = []
        runtimes = [-1]

    runtime = np.mean(runtimes)

    runtime = round(runtime, 2)

    if system == "influx" and len(query_data) > 0:
        query_data = [list(result) for result in query_data][0]
        # cast dict to tuples (key1,value1,key2 ,value2..
        query_data = [tuple(result.items())[:] for result in query_data]

    try:
        print(query_data)
        print("tries to convert query data to list")
        query_data = list(query_data)
    except:
        print("query data could not be converted to list")
        pass

    try:
        query_data = sorted(query_data, key=lambda x: x[0])
    except:
        pass

    QueryResult = namedtuple("QueryResult", "runtime query_data query runtimes")
    return QueryResult(runtime, query_data, parsed_query, runtimes)
