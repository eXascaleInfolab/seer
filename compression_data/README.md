# Compression Data Structure 

The ts contains folders for each data set containing folders for each feature type and a file description.txt containing the description of the dataset and a file containing the original dataset.
The compressions folder contains the compression results for each dataset (names need to match the dataset names).
For each dataset and system there is a system.txt file containing all the compression results for each feature in the dataset.

To upload a new DataSet you need to create a folder with the name of the dataset and add a file description.txt containing the description of the dataset and a file containing the original dataset.
To upload a new compression result you need to create a folder with the name of the dataset and add a file {system}.txt for each system containing all the compression results for each feature in the dataset.

## Example

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
