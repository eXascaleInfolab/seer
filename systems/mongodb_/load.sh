#!/bin/sh

# Load a commaseperated file into a mongodbdb database and measure the time it takes to load it

docker start mongodb
sleep 5
# THE FOLLOWING SCRIPT WILL SETUP AND LOAD D1

dataset="d1"
table_name="d1_test"
dataset_path="../../query_data/live_queries/"

current="$(pwd)"

# we need the file without header to specify the types

if [ -f "${dataset_path}${dataset}_no_header.csv" ]; then
    echo "headerless file exists."
else
  sed '1d' ${dataset_path}$dataset.csv > ${dataset_path}${dataset}_no_header.csv
fi

start_time=$(date +%s.%N)

docker cp ${dataset_path}${dataset}_no_header.csv mongodb:/tmp/$dataset.csv

## import the data
docker exec -it mongodb mongoimport -d $dataset -c $table_name --type csv --file /tmp/$dataset.csv  --columnsHaveTypes \
    -f "time.date(2006-01-02T15:04:05),id_station.string(),s0.double(),s1.double(),s2.double(),s3.double(),s4.double(),s5.double(),s6.double(),s7.double(),s8.double(),s9.double(),s10.double(),s11.double(),s12.double(),s13.double(),s14.double(),s15.double(),s16.double(),s17.double(),s18.double(),s19.double(),s20.double(),s21.double(),s22.double(),s23.double(),s24.double(),s25.double(),s26.double(),s27.double(),s28.double(),s29.double(),s30.double(),s31.double(),s32.double(),s33.double(),s34.double(),s35.double(),s36.double(),s37.double(),s38.double(),s39.double(),s40.double(),s41.double(),s42.double(),s43.double(),s44.double(),s45.double(),s46.double(),s47.double(),s48.double(),s49.double(),s50.double(),s51.double(),s52.double(),s53.double(),s54.double(),s55.double(),s56.double(),s57.double(),s58.double(),s59.double(),s60.double(),s61.double(),s62.double(),s63.double(),s64.double(),s65.double(),s66.double(),s67.double(),s68.double(),s69.double(),s70.double(),s71.double(),s72.double(),s73.double(),s74.double(),s75.double(),s76.double(),s77.double(),s78.double(),s79.double(),s80.double(),s81.double(),s82.double(),s83.double(),s84.double(),s85.double(),s86.double(),s87.double(),s88.double(),s89.double(),s90.double(),s91.double(),s92.double(),s93.double(),s94.double(),s95.double(),s96.double(),s97.double(),s98.double(),s99.double()"


end_time=$(date +%s.%N)
elapsed_time=$(echo "$end_time - $start_time" | bc)
echo "Loading time: $elapsed_time seconds" > loading_time_$table_name.txt


### create a index on the time field
#docker exec -it mongodb mongo $dataset --eval "db.$dataset.createIndex({'time': 1})"

echo "comression"
sh compression.sh


docker exec -it mongodb mongoimport -d $dataset -c $table_name$table_name --type csv --file /tmp/d1.csv  --columnsHaveTypes \
    -f "time.date(2006-01-02T15:04:05),id_station.string(),s0.double(),s1.double(),s2.double(),s3.double(),s4.double(),s5.double(),s6.double(),s7.double(),s8.double(),s9.double(),s10.double(),s11.double(),s12.double(),s13.double(),s14.double(),s15.double(),s16.double(),s17.double(),s18.double(),s19.double(),s20.double(),s21.double(),s22.double(),s23.double(),s24.double(),s25.double(),s26.double(),s27.double(),s28.double(),s29.double(),s30.double(),s31.double(),s32.double(),s33.double(),s34.double(),s35.double(),s36.double(),s37.double(),s38.double(),s39.double(),s40.double(),s41.double(),s42.double(),s43.double(),s44.double(),s45.double(),s46.double(),s47.double(),s48.double(),s49.double(),s50.double(),s51.double(),s52.double(),s53.double(),s54.double(),s55.double(),s56.double(),s57.double(),s58.double(),s59.double(),s60.double(),s61.double(),s62.double(),s63.double(),s64.double(),s65.double(),s66.double(),s67.double(),s68.double(),s69.double(),s70.double(),s71.double(),s72.double(),s73.double(),s74.double(),s75.double(),s76.double(),s77.double(),s78.double(),s79.double(),s80.double(),s81.double(),s82.double(),s83.double(),s84.double(),s85.double(),s86.double(),s87.double(),s88.double(),s89.double(),s90.double(),s91.double(),s92.double(),s93.double(),s94.double(),s95.double(),s96.double(),s97.double(),s98.double(),s99.double()"
