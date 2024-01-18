import json



def get_datasets_infos():
    with open('config/datasets.json', 'r') as file:
        datasets_info = json.load(file)
    return datasets_info

def get_datasets():
    datasets_info = get_datasets_infos()
    return [  (key,datasets_info[key]["title"]) for key in datasets_info.keys()]


def get_dataset_info(dataset):
    datasets_info = get_datasets_infos()
    if dataset not in datasets_info.keys():
        return {
            "title": "Custom Dataset",
            "description": "",
            "link": "-",
            "source": "",
        }
    return datasets_info[dataset]
