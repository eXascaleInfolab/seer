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
- Initialize the tool with offline and online results

```bash
sh setup/init_seer.sh
sh setup/migrate_query_data.sh
```
- After setting up the tool, you can access it by opening http://localhost:12007 in your browser. If the tool does not launch, please review the docker installation






## SEER Extension

### Add New Datasets
- Display and Generation: To add new Datasets to display and to run the new time series data generation follow the steps in [generation](generation/README.md).
- Compression: Follow the steps [here](compression_data/README.bd).

### Update Existing Results
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
  

### Add Precomputed Results
- **Offline**
1. Install the system following the TSM-Bench instructions
2. Add the name of the system to `utils/CONSTANTS.py` (Lines 8 and 9)
3. Add the name of the system to the import in `views/offline_queries_view.py` (Line 10)
4. Go to `views/offline_queries_view.py` and add the name of the system to systems (line 33)
5. Go to `djangoProject/models/load_query_data.py` and add the system to the systems list (line 6)
6. Load the query data into the django models
   ```bash
   sh setup/sh setup/migrate_query_data.sh
   ```
- **Online**
1. Install the system following the TSM-Bench instructions
2. Add the name of the system to `utils/CONSTANTS.py` (if not done in offline)
3. Add the name of the system to the import in `views/online_queries_view.py` (Line 6)
4. Go to `views/online_queries_view.py` and add the name of the system to systems (line 38)



###  Deploy New System/Configuration

The installation and loading of the systems for the live execution setup can be found [here](systems/README.md).

    

___

## Contributors

- Luca Althaus
- [Mourad Khayati](https://exascale.info/members/mourad-khayati/) (mkhayati@exascale.info)






