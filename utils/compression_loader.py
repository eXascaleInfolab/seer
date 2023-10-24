
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


def convert_compression_to_KB(compression_size):
    # handle Gib Kib Mib B KB MB
    if compression_size.endswith('B'):
        return int(compression_size[:-1]/1000)
    if compression_size.endswith('KB'):
        return int(compression_size[:-2])
    if compression_size.endswith('MB'):
        return int(compression_size[:-2])*1000
    if compression_size.endswith('GB'):
        return int(compression_size[:-2])*1000000
    if compression_size.endswith('Gib'):
        return int(compression_size[:-3])*134218
    if compression_size.endswith('Mib'):
        return int(compression_size[:-3])*131
    if compression_size.endswith('Kib'):
        return int(int(compression_size[:-3])/1.024)
    assert False , "Compression size not handled: " + compression_size



def load_systems_compression():
    path = os.path.join('compression_data', 'compressions')
    systems = {}
    for file in os.listdir(path):
        system_name = file.split('_')[0]
        with open(os.path.join(path, file), 'r') as f:
            for line in f.readlines():
                data_set , compression_size , loading_time = line.split(' ')
                compression_size = convert_compression_to_KB(compression_size)
                systems[system_name] = systems.get(system_name, {})
                systems[system_name][data_set] = (compression_size, loading_time)

    return systems


if __name__ == '__main__':
    print(load_compression_data_sets())
    print(load_systems_compression())