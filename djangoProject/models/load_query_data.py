"""
load data from server if needed
e.g
scp -r luca@diufrm110:/localdata/TSM-Bench/utils/full_results/d1/influx.csv  ~/PycharmProjects/djangoProject/query_data/offline_queries/d1/
"""
import struct

from djangoProject.models import QueryModel
import pandas as pd

def load_offline_query_data(systems=("timescaledb", "extremedb", "influx", "questdb", "clickhouse", "druid", "monetdb"),
                            datasets=("d1", "d2")):
    path = "query_data/offline_queries/"
    columns = ["runtime", "var", "query", "n_sensors", "n_stations", "timerange"]

    for dataset in datasets:
        dataset_path = f"{path}{dataset}/"
        for system in systems:
            try:
                file_path = f"{dataset_path}{system}.csv"
                df = pd.read_csv(file_path, names=columns, converters={'query': str.strip, "timerange": str.strip},
                                 skipinitialspace=True)

                for query in set(df["query"]):
                    q_m, _ = QueryModel.objects.get_or_create(query=query.strip(), system=system, dataset=dataset)
                    print(q_m)
                    data_str = df[df["query"] == query][
                        ["runtime", "var", "n_sensors", "n_stations", "timerange"]].to_csv(
                        index=False)
                    q_m.set_data(data_str)
            except Exception as e:
                print(e)
                print(f"error loading offline data {system} {dataset}")
