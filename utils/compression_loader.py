
from utils.CONSTANTS import compression_types , compressed_systems
import os
import pandas as pd

def df_to_highcharts(df,n_sensors=4):
    result = {}
    result["time"] = df["time"].tolist()
    for i in range(n_sensors):
        result["s"+str(i)] = df["s"+str(i)].tolist()
    return result

def load_compression_data_sets():
    #print(os.listdir())
    path = os.path.join('compression_data','ts')

    data_sets = {}
    for file in os.listdir(path):
        print(file)
        compression_type = "_".join(file.split('_')[:-1])
        compression_identifier = file.split('_')[-1].split('.')[0]
        data_sets[compression_type] = data_sets.get(compression_type, {})
        if file.endswith('.csv') and compression_type in compression_types:
            pandas_df = pd.read_csv(os.path.join(path, file))
            n, m = pandas_df.shape
            pandas_df = pandas_df.iloc[:min(n,500),:10]
            print(pandas_df)
            data_sets[compression_type][compression_identifier] = df_to_highcharts(pandas_df)
    return data_sets


def convert_compression_to_KB(compression_size):
    compression_size = compression_size.split("/")[0].strip()
    # handle Gib Kib Mib B KB MB
    print(compression_size)
    if compression_size.endswith('KiB'):
        return float(float(compression_size[:-3])*1.024)
    if compression_size.endswith('KB'):
        return float(compression_size[:-2])
    if compression_size.endswith('MB'):
        return float(compression_size[:-2])*1000
    if compression_size.endswith('GB'):
        return float(compression_size[:-2])*1000000
    if compression_size.endswith('GiB'):
        return float(compression_size[:-3])*134218
    if compression_size.endswith('MiB'):
        return float(compression_size[:-3])*131
    if compression_size.endswith('B'):
        return float(float(compression_size[:-1]) / 1000)
    if compression_size.endswith('K'):
        return float(float(compression_size[:-1]))
    if compression_size.endswith('G'):
        return float(float(compression_size[:-1])*1000000)
    if compression_size.endswith('M'):
        return float(float(compression_size[:-1])*1000)
    assert False , "Compression size not handled: " + compression_size



def load_systems_compression():
    path = os.path.join('compression_data', 'compressions')
    systems = {}
    for file in os.listdir(path):
        system_name = file.split('_')[0]
        if system_name not in compressed_systems:
            continue
        with open(os.path.join(path, file), 'r') as f:
            for line in f.readlines():
                data_set , compression_size , loading_time = line.split(' ')
                compression_size = convert_compression_to_KB(compression_size)
                loading_time = float(loading_time.strip()[:-1])
                systems[system_name] = systems.get(system_name, {})
                systems[system_name][data_set] = (compression_size, loading_time)

    return systems


if __name__ == '__main__':
    load_compression_data_sets()
    #print(load_systems_compression())