import datetime

from django.db import models
from django.utils.functional import cached_property


class QueryModel(models.Model):
    """
    system = system name e.g influx, timescaledb , druid , ...
    query = query name e.g q1,q2,q3,q4,q5,q6,q7]]
    dataset = dataset name e.g d1, d2
    data is of the form:
    runtime , var , n_sensors, n_stations , time range
    1  , 10 , 10 , 20 ,  month
    1  , 3 , 5 , 10 , week
    ...
    """

    system = models.CharField(max_length=100)
    query = models.CharField(max_length=100)
    dataset = models.CharField(max_length=100)
    data = models.TextField(default="runtime , var , n_sensors, n_stations , time range \n")

    def __str__(self):
        return self.system + " " + self.dataset + " " + self.query

    def set_data(self, data, override=False):
        if not override and len(self.data.split('\n')) > 1:
            self.data = data + "\n" + "\n".join(data.split('\n')[1:])
        else:
            self.data = data

        self.save()

    def get_query(self):
        return self.query

    def get_system(self):
        return self.system

    @property  # make it cached?
    def runtime_dict(self):
        print("computing runtime dict")
        data = self.data.split('\n')[1:]
        result_dict = {}
        for line in data:
            if line == "":
                continue
            line = line.split(',')
            result_dict[(int(line[2]), int(line[3]), line[4].strip())] = float(line[0])
        return result_dict

    def get_run_time(self, n_sensors, n_stations, time_range):
        runtime_dict = self.runtime_dict
        result = runtime_dict.get((n_sensors, n_stations, time_range), -1)
        if result == -1:
            print(f"Query {self.query} not found for system {self.system} with n_sensors {n_sensors} ,"
                  f" n_stations {n_stations} , time_range {time_range}")
        return result

    @classmethod
    def get_all_system_runtimes(cls, dataset, query, n_sensors, n_stations, time_range):
        from utils.CONSTANTS import SYSTEMS
        result = {}
        for system in SYSTEMS:
            try:
                q_m = cls.objects.get(system=system, query=query, dataset=dataset)
                result[system] = q_m.get_run_time(n_sensors, n_stations, time_range)
            except QueryModel.DoesNotExist:
                print("system or query not found")
                result[system] = -1

        return result


"""for testing 
python3 manage.py  shell
from djangoProject.models.query_model import QueryModel
QueryModel.objects.all()
QueryModel.objects.filter(system="influx" , query="Q1")
QueryModel.objects.get(system="influx", query="q1")
QueryModel.objects.get(system="influx", query="q1").get_run_time(10,20,"month")
QueryModel.get_all_system_runtimes("d1" ,  "q1" , 10 , 20 , "month")
"""
