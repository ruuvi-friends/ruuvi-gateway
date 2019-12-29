# By default gets them from OS env for docker conveninence
import os 

TIMESERIES_NAME = os.getenv('TIMESERIES_NAME') or "ruuvi-sensors"


BASIC_AUTH_FORCE = os.getenv('BASIC_AUTH_FORCE', False)
BASIC_AUTH_USERNAME = os.getenv('BASIC_AUTH_USERNAME')
BASIC_AUTH_PASSWORD = os.getenv('BASIC_AUTH_PASSWORD')


# INFLUXDB PARAMETERS
INFLUX_DB_NAME = os.getenv('INFLUX_DB_NAME')
INFLUX_URL = os.getenv('INFLUX_URL', 'localhost')
INFLUX_PORT = os.getenv('INFLUX_PORT')
INFLUX_USER = os.getenv('INFLUX_USER')
INFLUX_PASSWORD = os.getenv('INFLUX_PASSWORD')
