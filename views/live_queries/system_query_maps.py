"""
    This file contains the functions to run a query on a system.

    See the __init__.py file in the Systems. How the systems and the host are inferred.
    The host of the system is defined in the host dict. Depending if the tool is run using docker or with the basic
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
from systems import get_system_module, get_host, get_table_name


def run_query(system, q_n, rangeL, rangeUnit, n_st, n_s, n_it=1, dataset="d1"):
    print("running query\n", q_n, rangeL, rangeUnit, n_st, n_s, "on system", system)





    system_module = get_system_module(system)
    host = get_host(system)
    dataset = get_table_name(system)
    print("system", system ,"aaa")
    print("host", host)
    print("data_table", dataset)

    query_template = load_query(system, q_n)
    query_template = query_template.replace("<db>", dataset)

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
                runtimes.append(runtime*2)

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
