import os
def get_system_folders():
    folders = os.listdir(os.path.dirname(__file__))
    print(folders)
    # exclude .py  .md files .json  utils and folders ending with _
    return [folder for folder in folders if not
            (folder.endswith(".py") or folder.endswith(".json") or
             folder.endswith(".md") or folder.endswith("_") or folder == "utils")]

def get_system_module(system_name):
    return {folder: __import__(f"systems.{folder}", fromlist=["systems"]) for folder in get_system_folders()}[system_name]

def get_host(system_name):
    """
    {"clickhouse": "clickhouse" if os.getenv("using_docker") else "localhost",
            "timescaledb": "timescaledb" if os.getenv("using_docker") else "localhost",
            "monetdb": os.getenv("DOCKER_HOST", "localhost"),
            "mongodb": os.getenv("DOCKER_HOST", "localhost"),
            }
    """
    # handle the case when the system is included in the docker-compose file
    if system_name in ("clickhouse_v2","clickhouse"):
        return "clickhouse" if os.getenv("using_docker") else "localhost"
    elif system_name == "timescaledb":
        return "timescaledb" if os.getenv("using_docker") else "localhost"
    # handle the case when the system is run on the local machine
    return os.getenv("DOCKER_HOST", "localhost")


def get_table_name(system_name):
    # read table_map.json
    import json
    with open("systems/table_map.json", "r") as f:
        table_map = json.load(f)
    return table_map[system_name]

#
# system_module_map = {"clickhouse": clickhouse,
#                      "timescaledb": timescaledb,
#                      "influx": influx,
#                      "monetdb": monetdb,
#                      "mongodb": mongodb,
#                      }