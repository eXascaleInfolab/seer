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

def query_parser(query, dataset ,  rangeL, rangeUnit, n_st, n_s, seed=100 , system = None):
    random.seed(seed)
    date = random_date("2019-04-30T00:00:00", "2019-04-01T00:00:00", set_date[(int(rangeL) * 1) % 500],
                       dform='%Y-%m-%dT%H:%M:%S')

    query = query.replace("<db>",dataset)
    query = query.replace("<timestamp>", date)
    query = query.replace("<range>", str(rangeL))
    query = query.replace("<rangesUnit>", rangeUnit)

    # sensors
    li = ['s' + str(z) for z in random.sample(range(100), n_s)]
    q = li[0]
    q_filter = '(' + li[0] + ' > 0.95' + ')'

    ########## Check this
    q_avg = 'avg(' + li[0] + ')'
    for j in li[1:]:
        q += ', ' + j
        # q_filter += ' OR ' + j + ' > 0.95'
        q_avg += ', ' + 'avg(' + j + ')'

    assert q == ", ".join(li)
    assert q_avg == ", ".join([f"avg({s_})" for s_ in li])

    #############
    query = query.replace("<sid>", q)
    query = query.replace("<sfilter>", q_filter)
    query = query.replace("<avg_s>", q_avg)
    query = query.replace("<sid1>", "s1")
    query = query.replace("<sid2>", "s2")

    # stations with special interpolation case of clickhouse
    if "fill step" in query.lower() and system == "clickhouse":
        if n_st == 1:
            q = "('" + 'st' + str(random.sample(range(10), 1)[0]) + "')"
            query = query.replace("<stid>", q)

        else:
            station_list = ['st' + str(z) for z in random.sample(range(10), n_st)]  # sample stations
            fill_commands = []  # queries to unite
            for station in station_list:
                q = f"('{station}')"
                station_fill = query.replace("<stid>", q).replace(";", "")
                fill_commands.append(station_fill)

            query = "SELECT * FROM (" + " UNION ALL ".join(fill_commands) + ")"

    else:  # normal station insertion
        station_list = ['st' + str(z) for z in random.sample(range(10), n_st)]  # sample stations
        q = "(" + ', '.join(["'" + j + "'" for j in station_list]) + ")"
        query = query.replace("<stid>", q)


    # assert "<" not in query and ">" not in query , query

    return query
