# Setup 

modify the .env file
- specify a django key
- provide the path to your dataset folder (used for the live evaluation)
```bash
vim .env
```  

## launch

```bash
docker-compose up -d --build
```  
The Website should be running under http://localhost:12007

## Collect static files, create admin account and migrate the database

```bash
container_id=$(docker ps | grep app | awk '{print $1}') #or find id of "app" with docker ps
echo "$container_id"
docker exec -it $container_id  python3 manage.py collectstatic
docker exec -it $container_id  python3 manage.py makemigrations
docker exec -it $container_id  python3 manage.py migrate
docker exec -it $container_id  python3 manage.py createsuperuser

docker restart  $container_id
```

## Load query data into django models

Open the django shell
```bash
docker exec -it $container_id python3 manage.py shell
```  

Inside the shell execute the following commands:
```python
from djangoProject.models.load_query_data import load_offline_query_data
load_offline_query_data()
```



## Live Evaluation  setup

Create dataset d1 that is used for the live query evaluation.
```shell
cd query_data/live_queries
sh build_d1.sh
cd ../..
```

### Clickhouse
Clickhouse is already include in the docker-compose.yml file.

Define the dataset:
```bash
dataset='d1'
source .env #read the Dataset path from the env file, timescale db does this when docker ist started already
```  

Optional drop the table if it exists
```bash 
docker exec -it clickhouse-demo clickhouse-client --query "DROP TABLE IF EXISTS $dataset;"
```  

Create the Table:
```bash

docker exec -it clickhouse-demo clickhouse-client --query "CREATE TABLE IF NOT EXISTS $dataset (  \
        time DateTime64(9), id_station String, s0 Float32 , s1 Float32 , s2 Float32 , s3 Float32 , s4 Float32 , s5 Float32 , s6 Float32 , s7 Float32 , s8 Float32 , s9 Float32 , s10 Float32 , s11 Float32 , s12 Float32 , s13 Float32 , s14 Float32 , s15 Float32 , s16 Float32 , s17 Float32 , s18 Float32 , s19 Float32 , s20 Float32 , s21 Float32 , s22 Float32 , s23 Float32 , s24 Float32 , s25 Float32 , s26 Float32 , s27 Float32 , s28 Float32 , s29 Float32 , s30 Float32 , s31 Float32 , s32 Float32 , s33 Float32 , s34 Float32 , s35 Float32 , s36 Float32 , s37 Float32 , s38 Float32 , s39 Float32 , s40 Float32 , s41 Float32 , s42 Float32 , s43 Float32 , s44 Float32 , s45 Float32 , s46 Float32 , s47 Float32 , s48 Float32 , s49 Float32 , s50 Float32 , s51 Float32 , s52 Float32 , s53 Float32 , s54 Float32 , s55 Float32 , s56 Float32 , s57 Float32 , s58 Float32 , s59 Float32 , s60 Float32 , s61 Float32 , s62 Float32 , s63 Float32 , s64 Float32 , s65 Float32 , s66 Float32 , s67 Float32 , s68 Float32 , s69 Float32 , s70 Float32 , s71 Float32 , s72 Float32 , s73 Float32 , s74 Float32 , s75 Float32 , s76 Float32 , s77 Float32 , s78 Float32 , s79 Float32 , s80 Float32 , s81 Float32 , s82 Float32 , s83 Float32 , s84 Float32 , s85 Float32 , s86 Float32 , s87 Float32 , s88 Float32 , s89 Float32 , s90 Float32 , s91 Float32 , s92 Float32 , s93 Float32 , s94 Float32 , s95 Float32 , s96 Float32 , s97 Float32 , s98 Float32 , s99 Float32 \
        ) ENGINE = MergeTree() PARTITION BY toYYYYMMDD(time) ORDER BY (id_station, time) Primary key (id_station, time);"

```  

Load the data:
```bash
docker exec -i clickhouse-demo clickhouse-client --format_csv_delimiter="," -q "INSERT INTO $dataset FORMAT CSV" < $DATASET_PATH/$dataset.csv
```  

You can check that the data is loaded correctly by checking its compression in the Database
```bash
docker exec -it clickhouse-demo clickhouse-client --query "SELECT table, formatReadableSize(sum(bytes)) as size FROM system.parts WHERE active AND table='$dataset' GROUP BY table;"
```  

###  Monetdb
```bash

cd systems/monetdb
sh install.sh 
sh launch.sh
sh load.sh 
cd ../..
```  


###  Timescaledb
In the docker compose file make sure the datasets volume is
mapped to the volume where the dataset is located.

```shell
dataset='d1'

docker exec -it timescaledb-demo psql -U postgres -c  "CREATE TABLE $dataset ( time TIMESTAMP NOT NULL, id_station TEXT NOT NULL, s0 DOUBLE PRECISION , s1 DOUBLE PRECISION , s2 DOUBLE PRECISION , s3 DOUBLE PRECISION , s4 DOUBLE PRECISION , s5 DOUBLE PRECISION , s6 DOUBLE PRECISION , s7 DOUBLE PRECISION , s8 DOUBLE PRECISION , s9 DOUBLE PRECISION , s10 DOUBLE PRECISION , s11 DOUBLE PRECISION , s12 DOUBLE PRECISION , s13 DOUBLE PRECISION , s14 DOUBLE PRECISION , s15 DOUBLE PRECISION , s16 DOUBLE PRECISION , s17 DOUBLE PRECISION , s18 DOUBLE PRECISION , s19 DOUBLE PRECISION , s20 DOUBLE PRECISION , s21 DOUBLE PRECISION , s22 DOUBLE PRECISION , s23 DOUBLE PRECISION , s24 DOUBLE PRECISION , s25 DOUBLE PRECISION , s26 DOUBLE PRECISION , s27 DOUBLE PRECISION , s28 DOUBLE PRECISION , s29 DOUBLE PRECISION , s30 DOUBLE PRECISION , s31 DOUBLE PRECISION , s32 DOUBLE PRECISION , s33 DOUBLE PRECISION , s34 DOUBLE PRECISION , s35 DOUBLE PRECISION , s36 DOUBLE PRECISION , s37 DOUBLE PRECISION , s38 DOUBLE PRECISION , s39 DOUBLE PRECISION , s40 DOUBLE PRECISION , s41 DOUBLE PRECISION , s42 DOUBLE PRECISION , s43 DOUBLE PRECISION , s44 DOUBLE PRECISION , s45 DOUBLE PRECISION , s46 DOUBLE PRECISION , s47 DOUBLE PRECISION , s48 DOUBLE PRECISION , s49 DOUBLE PRECISION , s50 DOUBLE PRECISION , s51 DOUBLE PRECISION , s52 DOUBLE PRECISION , s53 DOUBLE PRECISION , s54 DOUBLE PRECISION , s55 DOUBLE PRECISION , s56 DOUBLE PRECISION , s57 DOUBLE PRECISION , s58 DOUBLE PRECISION , s59 DOUBLE PRECISION , s60 DOUBLE PRECISION , s61 DOUBLE PRECISION , s62 DOUBLE PRECISION , s63 DOUBLE PRECISION , s64 DOUBLE PRECISION , s65 DOUBLE PRECISION , s66 DOUBLE PRECISION , s67 DOUBLE PRECISION , s68 DOUBLE PRECISION , s69 DOUBLE PRECISION , s70 DOUBLE PRECISION , s71 DOUBLE PRECISION , s72 DOUBLE PRECISION , s73 DOUBLE PRECISION , s74 DOUBLE PRECISION , s75 DOUBLE PRECISION , s76 DOUBLE PRECISION , s77 DOUBLE PRECISION , s78 DOUBLE PRECISION , s79 DOUBLE PRECISION , s80 DOUBLE PRECISION , s81 DOUBLE PRECISION , s82 DOUBLE PRECISION , s83 DOUBLE PRECISION , s84 DOUBLE PRECISION , s85 DOUBLE PRECISION , s86 DOUBLE PRECISION , s87 DOUBLE PRECISION , s88 DOUBLE PRECISION , s89 DOUBLE PRECISION , s90 DOUBLE PRECISION , s91 DOUBLE PRECISION , s92 DOUBLE PRECISION , s93 DOUBLE PRECISION , s94 DOUBLE PRECISION , s95 DOUBLE PRECISION , s96 DOUBLE PRECISION , s97 DOUBLE PRECISION , s98 DOUBLE PRECISION , s99 DOUBLE PRECISION );"
```

```shell 
docker exec -it timescaledb-demo psql -U postgres -c  "SELECT create_hypertable('$dataset', 'time', chunk_time_interval=>'7 days'::INTERVAL);"
```

```shell
docker exec -it timescaledb-demo psql -U postgres -c "COPY $dataset FROM '/datasets/$dataset.csv' DELIMITER ',' CSV HEADER;";
```

```shell
docker exec -it timescaledb-demo psql -U postgres -c "SELECT hypertable_size('$dataset') ;"
```


### Influx (To be tested)
Our Influx version requires python3.8 That is why we load it directly in the main docker-container

```shell
cd systems/influx
chmod +x install.sh
chmod +x launch.sh
chmod +x load.sh
chmod +x compression.sh

container_id=$(docker ps | grep app | awk '{print $1}') #or find id of "app" with docker ps
echo "$container_id"

docker exec -u root $container_id /usr/src/app/systems/influx/install.sh
docker exec -u root $container_id /usr/src/app/systems/influx/launch.sh

#check if it works
curl -G http://localhost:8083/query --data-urlencode "q=SHOW DATABASES"


docker exec -u root $container_id /usr/src/app/systems/influx/load.sh

docker exec $container_id  /usr/src/app/systems/influx/compression.sh
```