
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
sh setup/init_tool.sh
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


### Adding data to the tool
The description on how to add the feature compression datasets can be found here  [here](compression_data/README.md).
The description add data to the time series generation can be found here  [here](generation/README.md).


## Useful commands

### Open the django shell to run python code in tools environment

```bash
docker exec -it $container_id python3 manage.py shell
```
