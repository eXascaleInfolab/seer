import os
import json

def get_system_map():
    with open("systems/table_map.json", "r") as file:
        data = json.load(file)
    return data

def get_system_names():
    print(get_system_map().keys())
    return list(get_system_map().keys())

def get_system_folders():
    folders = os.listdir(os.path.dirname(__file__))
    print(folders)
    # exclude .py  .md files .json  utils and folders ending with _
    return [folder for folder in folders if not
            (folder.endswith(".py") or folder.endswith(".json") or
             folder.endswith(".md") or folder.endswith("_") or folder == "utils")]

def get_system_folder(system_name):
    system_folder =  get_system_map()[system_name]["folder"]
    return system_folder

def get_system_module(system_name):
    system_folder =  get_system_folder(system_name)
    return __import__(f"systems.{system_folder}", fromlist=["systems"])

def get_host(system_name):
    host = get_system_map()[system_name]["host"]
    if host == "localhost":
        host = os.getenv("DOCKER_HOST", "localhost")
    return host

def get_table_name(system_name , table = "d1"):
    return  get_system_map()[system_name][table]