
import os
from ruuvi_gateway.utils import logger
from ruuvi_gateway.adapters import BaseAdapter
from influxdb import InfluxDBClient

class InfluxAdapter(BaseAdapter):
    """
    A connection adapter for Influx DB
    """

    def __init__(self, config):
        self.TIMESERIES_NAME = config.get('TIMESERIES_NAME', None)
        self.INFLUX_DB_NAME = config.get('INFLUX_DB_NAME', None)
        self.INFLUX_URL = config.get('INFLUX_URL', '127.0.0.1')
        self.INFLUX_PORT = config.get('INFLUX_PORT', 8086)
        self.INFLUX_USER = config.get('INFLUX_USER', None)
        self.INFLUX_PASSWORD = config.get('INFLUX_PASSWORD', None)

    def is_ready(self):
        return self.INFLUX_DB_NAME and self.TIMESERIES_NAME

    def connect(self):
        self.client = InfluxDBClient(
            host=self.INFLUX_URL, port=self.INFLUX_PORT,
            username=self.INFLUX_USER, password=self.INFLUX_PASSWORD,
            database=self.INFLUX_DB_NAME
        )

        existing_databases = self.client.get_list_database()
        if self.INFLUX_DB_NAME not in list(db['name'] for db in existing_databases):
            # Create if doesn't exist
            self.client.create_database(self.INFLUX_DB_NAME)

    def datapoint_to_influx_dict(self, datapoint):

        print(datapoint.sender_data)
        tags = {}
        tags.update(datapoint.tag_data)
        tags["sender_device_id"] = datapoint.sender_data['device_id']

        fields_data = datapoint.sensor_data
        fields_data["sender_battery_level"] = datapoint.sender_data.get('battery_level', None)
        
        sender_location_data = datapoint.sender_data.get('location', None)
        
        if sender_location_data:
            fields_data["sender_latitude"] = sender_location_data.get('latitude', None)
            fields_data["sender_longitude"] = sender_location_data.get('longitude', None)
            fields_data["sender_location_accuracy"] = sender_location_data.get('accuracy', None)
            # Currently not supporting location of sender.

        influx_datapoint = {
                "time": datapoint.iso_timestamp,
                "measurement": self.TIMESERIES_NAME,
                "tags": tags,
                "fields": fields_data
            }
        return influx_datapoint

    def push_metrics(self, metrics):
        logger.info("Pushing metrics to InfluxDB")
        influx_datapoints = [self.datapoint_to_influx_dict(metric) for metric in metrics]
        self.client.write_points(influx_datapoints)

    def connect_and_push_metrics(self, metrics):
        self.connect()
        self.push_metrics(metrics)