# SEER

SEER is an online tool to evaluate the performance of time series database systems on large datasets.
The tool builds upon our TSM-Bench benchmark [TSM-Bench: Benchmarking Time Series Database Systems for Monitoring Applications, PVLDB'23](https://www.vldb.org/pvldb/vol16/p3363-khelifati.pdf).
SEER compares seven Time Series Database Systems (TSDBs) using a mixed set of workloads. It implements a novel data generation method that augments seed real-world time series datasets, enabling realistic and scalable benchmarking. 
<!---
Technical details can be found in the paper SEER: An End-to-End Toolkit to Evaluate Time Series Database Systems, SIGMOD'24
-->
- List of benchmarked systems: [ClickHouse](https://clickhouse.com/), [Druid](https://druid.apache.org/), [eXtremeDB](https://www.mcobject.com/)*, [InfluxDB](https://docs.influxdata.com/influxdb/v1.7/), [MonetDB](https://www.monetdb.org/easy-setup/), [QuestDB](https://questdb.io/), [TimescaleDB](https://www.timescale.com/).
- SEER evaluates bulk-loading,  storage performance, offline/online query performance, and the impact of time series features on compression.
- The tool uses two datasets for the evaluation: *D-LONG [d1] and D-MULTI [d2]*. The evaluated datasets can be found [here](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/datasets).
- <sup>*</sup>**Note**: Due to license restrictions, we can only share the evaluation version of extremeDB. The results between the benchmarked and the public version might diverge. 


 SEER was created at the eXascale Infolab, a research group at the University of Fribourg, Switzerland. 

___


##  Prerequisites

- Ubuntu 20 (including Ubuntu derivatives, e.g., Xubuntu) 
- Clone this repository 

[//]: # (- Install Docker and Docker-Compose)

[//]: # (___)


## Setup
- Install Docker and Docker-Compose if not already installed
```bash
sh setup/install_docker.sh
```  

- Build the app and start it
```bash
docker-compose up -d --build
```

- After setting up the frontend and backend, you can access the application by opening http://localhost:12007 in your browser. If the tool does not launch, please review the docker installation


##  Upload Results

```bash
sh setup/init_seer.sh
sh setup/migrate_query_data.sh
```


___

## Contributors

Mourad Khayati (mkhayati@exascale.info) and Luca Althaus.

[//]: # (### Load query data into django models)

[//]: # (Open the django shell)

[//]: # (```bash)

[//]: # (docker exec -it $container_id python3 manage.py shell)

[//]: # (```)

[//]: # (Inside the shell execute the following commands:)

[//]: # (```python)

[//]: # (from djangoProject.models.load_query_data import load_offline_query_data)

[//]: # (load_offline_query_data&#40;&#41;)

[//]: # (```)

[//]: # (Quit the django shell using Ctr-Z.)

<!---



###  Live Systems Configuration

The installation and loading of the systems for the live execution setup can be found [here](systems/README.md).


## SEER Extension

### New Datasets

- To add datasets to the feature compression: [link](compression_data/README.md).

- To add datasets to the time series generation: [link](generation/README.md).

### New System's results
- offline
1. Go to `query_data/offline_queries` folder:
2. Select the dataset folder and add the results of the system in a file system_name.csv
    the file contains the following columns:
    - runtime: the computed runtime of the query
    - variance: the variance of the query
    - query: the query e.g q4
    - n_s : the number of sensors
    - n_st : the number of stations
    - timerange : the time range of the query
3. Go to `views/offline_queries_view.py` update the context of the query class and add the system to systems (line 32).
4. Go to "djangoProject/models/load_query_data.py" and add the system to the systems list (line 10).
5. Load the query data into the django models
   ```bash
   sh setup/sh setup/migrate_query_data.sh
   ```

- online
1. Go to `query_data/online_queries` folder:
2. Select the dataset folder and add the results of the system in a file system_name.csv
    the file contains the following columns:
    - runtime: the computed runtime of the query
    - variance: the variance of the query
    - query: the query e.g q4
    - n_s : the number of sensors
    - n_st : the number of stations
    - timerange : the time range of the query
    - insertion_rate: the ingestion rate 
3. Go to `views/online_queries_view.py` update the context of the query class and add the system to systems (line 38).

## Useful commands

### Open the django shell to run python code in tools environment

```bash
docker ps
```

Replace $container_id with the id of the app container and run 

```bash
docker exec -it $container_id python3 manage.py shell
```
-->

