# Steps
1. Go to `compression_data/ts/` folder:

2. Create a folder with the name of the dataset  and add the following files
   - description.txt: contains the description of the dataset
   - original.txt: contains the original data
     
3. For each feature, create a folder with the name of the feature and the datasets with the feature level
4. Go to `compression_data/compressions/` folder
5. Create a folder with the name of your dataset
6. For each system, add the files that contain the compression results.

# Folder Structure Example
```
comressions
├── conductivity
│   ├── clickhouse.txt
│   ├── druid.txt
│   ├── influx.txt
│   ├── timescaledb.txt
ts
├── conductivity
│   ├── description.txt
│   ├── original.csv
│   ├── outliers
│   │   ├── outliers_1.csv
│   │   ├── outliers_2.csv
│   │   ├── outliers_5.csv
│   │   ├── outliers_10.csv
│   ├── repeats
│   │   ├── repeats_1.csv
│   │   ├── ...
```
