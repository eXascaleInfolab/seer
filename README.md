
# SEER

SEER is an online tool to evaluate the performance of time series database systems on large datasets.
This tool was created at the eXascale Infolab, a research group at the University of Fribourg, Switzerland. 

## Setup 

Clone this repository.

### launch
```bash
docker-compose up -d --build
```  
The Website should be running under http://localhost:12007


### Collect static files and initialize django models

```bash
container_id=$(docker ps | grep app | awk '{print $1}') #or find id of "app" using docker ps
echo "$container_id"
docker exec -it $container_id  python3 manage.py collectstatic
docker exec -it $container_id  python3 manage.py makemigrations
docker exec -it $container_id  python3 manage.py migrate

docker exec -it $container_id  python3 manage.py createsuperuser (optional)
```

### Load query data into django models
Open the django shell
```bash
docker exec -it $container_id python3 manage.py shell
```
Inside the shell execute the following commands:
```python
from djangoProject.models.load_query_data import load_offline_query_data
load_offline_query_data()
```
Quit the django shell using Ctr-Z.


###  Live Systems and compression setup 
Installing and loading the systems for the Live Execution Setup can be found [here](systems/README.md).
The descrition on how to add the feature compression datasets can be found here  [here](compression_data/README.md).

