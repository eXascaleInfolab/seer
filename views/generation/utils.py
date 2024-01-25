import json
import os


path = "generation/data"

def store_description(description: dict):
    title = description["title"]
    with open(f'{path}/{title}/description.json', 'w') as file:
        json.dump(description, file, indent=4)

def get_datasets_infos():
    dataset_folders = os.listdir(path)
    print("loading dataset infos" , dataset_folders)

    datasets_info = {}
    for dataset in dataset_folders:
        with open(f"{path}/{dataset}/description.json", 'r') as description_file:
            try:
                datasets_info[dataset] = json.load(description_file)
            except:
                print("error loading description file for" , dataset)
                datasets_info[dataset] = {
                    "title": dataset,
                    "description": "",
                    "link": "-",
                    "source": "",
                }
    return datasets_info

def get_datasets():
    datasets_info = get_datasets_infos()
    return [  (key,datasets_info[key]["title"]) for key in datasets_info.keys()]


def get_dataset_info(dataset):
    datasets_info = get_datasets_infos()
    if dataset not in datasets_info.keys():
        print("dataset not found")
        return {
            "title": "Custom Dataset",
            "description": "No description available",
            "link": "",
            "source": "missing",
        }
    return datasets_info[dataset]
