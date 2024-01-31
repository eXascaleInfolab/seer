
# SEER

SEER is an online tool to evaluate the performance of time series database systems on large datasets.
This tool was created at the eXascale Infolab, a research group at the University of Fribourg, Switzerland. 

## Setup
___

[//]: # (###  Prerequisites)

[//]: # ([//]: # &#40;- Ubuntu 20 &#40;including Ubuntu derivatives, e.g., Xubuntu&#41;; 128 GB RAM&#41;)
[//]: # (- Clone this repository )

[//]: # (- Install Docker and Docker-Compose)

[//]: # (___)


### launch
- Install Docker and Docker-Compose if not already installed
```bash
sh setup/install_docker.sh
```  

- Build the app and start it
```bash
docker-compose up -d --build
```

- Launch the tool via http://localhost:12007. If the tool is not available, make sure that docker is properly installed


### Collect static files and initialize django models

```bash
sh setup/init_seer.sh
sh setup/migrate_query_data.sh
```

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


###  Live Systems Configuration

The installation and loading of the systems for the live execution setup can be found [here](systems/README.md).


## SEER Extension

### New Datasets

- To add datasets to the feature compression: [link](compression_data/README.md).

- To add datasets to the time series generation: [link](generation/README.md).

### New Systems' results
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
