import datetime
from django.db import models

class QueryModel(models.Model):
    system = models.CharField(max_length=100)
    query = models.CharField(max_length=100)
    data = models.TextField(default="")
    dataset = models.CharField(max_length=100)
    def __str__(self):
        return self.system + " " + self.query + " " + str(self.data)

    def get_data(self):
        return self.data

    def get_query(self):
        return self.query

    def get_system(self):
        return self.system


