# SEER

SEER is an online tool for evaluating the performance of seven Time Series Database Systems (TSDBs) using a mixed set of workloads. The tool builds upon our TSM-Bench benchmark [TSM-Bench: Benchmarking Time Series Database Systems for Monitoring Applications, PVLDB'23](https://www.vldb.org/pvldb/vol16/p3363-khelifati.pdf). SEER implements an end-to-end pipeline for database benchmarking, from data generation and workload evaluation to feature contamination. 
Technical details can be found in the paper SEER: An End-to-End Toolkit for Benchmarking Time Series Database Systems in Monitoring Applications, PVLDB'24
- List of benchmarked systems: [ClickHouse](https://clickhouse.com/), [Druid](https://druid.apache.org/), [eXtremeDB](https://www.mcobject.com/)*, [InfluxDB](https://docs.influxdata.com/influxdb/v1.7/), [MonetDB](https://www.monetdb.org/easy-setup/), [QuestDB](https://questdb.io/), [TimescaleDB](https://www.timescale.com/).
- SEER evaluates time series generation, offline/online query performance, and the impact of time series features on storage.
- SEER uses various hydrological datasets provided by the Swiss Federal Office for the Environment (FOEN). The evaluated datasets can be found [here](https://github.com/eXascaleInfolab/TSM-Bench/tree/main/datasets).
- <sup>*</sup>**Note**: Due to license restrictions, we can only share the evaluation version of extremeDB. 


 SEER was created at the eXascale Infolab, a research group at the University of Fribourg, Switzerland, under the direction of Dr. Mourad Khayati. 

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

- After setting up the tool, you can access it by opening http://localhost:12007 in your browser. If the tool does not launch, please review the docker installation


##  Upload Results

```bash
sh setup/init_seer.sh
sh setup/migrate_query_data.sh
```
___

## Contributors

- Luca Althaus
- [Mourad Khayati](https://exascale.info/members/mourad-khayati/) (mkhayati@exascale.info)

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


### Adding New Results
- **Offline**
1. Go to `query_data/offline_queries` folder
2. Select the dataset folder and add the results of the system in a file named `system_name.csv`. The file contains the following columns:
    - runtime: the computed runtime of the query
    - variance: the variance of the query
    - query: the query number (e.g., q4)
    - n_s : the number of sensors
    - n_st : the number of stations
    - timerange : the time range of the query
- **Online**
1. Go to `query_data/online_queries` folder:
2. Select the dataset folder and add the results of the system in a file named `system_name.csv`. The file contains the following columns:
    - runtime: the computed runtime of the query
    - variance: the variance of the query
    - query: the query number (e.g., q4)
    - n_s : the number of sensors
    - n_st : the number of stations
    - timerange : the time range of the query
    - insertion_rate: the ingestion rate 
    

### Adding New System Configuration
- **Offline**
1. Install the system following the TSM-Bench instructions
2. Go to `views/offline_queries_view.py` update the context of the query class and add the system to systems (line 32).
3. Add the name of the system to `utils/CONSTANTS.py` and to `views/offline_queries_view.py` (Line 10)
4. Go to "djangoProject/models/load_query_data.py" and add the system to the systems list (line 6).
5. Load the query data into the django models
   ```bash
   sh setup/sh setup/migrate_query_data.sh
   ```
- **Online**
1. Install the system following the TSM-Bench instructions
2. Go to `views/online_queries_view.py` and update the context of the query class by adding the system to systems (line 38).
3. Add the name of the system to `utils/CONSTANTS.py` (if not done in offline) and to `views/offline_queries_view.py` (Line 6)


### Adding New Datasets
- Display: 

- Generation:

- Compression: follow the steps in `https://github.com/eXascaleInfolab/seer/tree/master/compression_data`

-->

