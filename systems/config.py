"""
Configuration of the live systems.

live_systems Example:
 live_systems = {"clickhouse_no_time":
                     {"d1": "d1_test",
                      "folder": "clickhouse",  # folder in systems/ where all files are stored_ queries.sql,  ..
                      "description" : "Clickhouse system when dropping the time index.",
                      }
}
"""

live_systems = {"clickhouse_no_time": # name of the system
                    {"d1": "d1_test", # map d1 to d1_test where the configuration is different
                     "folder": "clickhouse",  # folder in systems/ where all files are stored_ queries.sql,  ..
                     "description": "Clickhouse system where dropping the time index.",
                     "host" : "clickhouse",
                     }
                }

# system info button message
SYSTEM_MESSAGE = "Due to the limited resources of the server, we can not run all systems at the same time."
