DRUID = "druid"
QUESTDB = "questdb"
INFLUX = "influx"
TIMESCALEDB = "timescaledb"
MONETDB = "monetdb"
EXTREMEDB = "extremedb"
CLICKHOUSE = "clickhouse"

SYSTEMS  = (DRUID, QUESTDB, CLICKHOUSE, INFLUX, TIMESCALEDB, MONETDB, EXTREMEDB)

compression_types = ('repeats', 'scarsity',"delta")#'delta' , "outliers"
compressed_systems = (TIMESCALEDB, DRUID, CLICKHOUSE, INFLUX)
