
from utils.CONSTANTS import compression_types
import os
import pandas as pd

def df_to_highcharts(df,n_sensors=4):
    result = {}
    result["time"] = df["time"].tolist()
    for i in range(n_sensors):
        result["s"+str(i)] = df["s"+str(i)].tolist()
    return result

def load_compression_data_sets():
    print(os.listdir())
    path = os.path.join('compression_data','ts')

    data_sets = {}
    for file in os.listdir(path):
        print(file)
        compression_type = "_".join(file.split('_')[:-1])
        compression_identifier = file.split('_')[-1].split('.')[0]
        data_sets[compression_type] = data_sets.get(compression_type, {})
        if file.endswith('.csv') and compression_type in compression_types:
            pandas_df = pd.read_csv(os.path.join(path, file))
            data_sets[compression_type][compression_identifier] = df_to_highcharts(pandas_df)
    return data_sets


if __name__ == '__main__':
    print(load_compression_data_sets())