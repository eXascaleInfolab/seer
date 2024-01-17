import os
import pandas as pd

directory = "raw_data"
folders = os.listdir(directory)

pattern = "Wassertemp"

for folder in folders:
    print("folder", folder)
    for file in os.listdir(directory+"/"+folder):
        if pattern in file:
            ts = []
            with open(directory+"/"+folder+"/"+file, encoding='utf-8', errors='ignore') as f:
                data = f.readlines()
                for line in data[9:]:
                    #extract 3 last column seperated by ;
                    line = line.split(";")
                    value = float(line[-2])
                    ts.append(line)
            print(len(ts))
        else:
            continue
