
import os
import csv
from datetime import datetime
from ruuvi_gateway.utils import logger
from ruuvi_gateway.adapters import BaseAdapter

FILED_NAMES = [
        # Tag data 
        "timestamp",
        "tag_id",
        "name",
        "favorite",

        # Sensor data
        "humidity",
        "pressure",
        "temperature",
        "accel_x",
        "accel_y",
        "accel_z",
        "voltage",
        "rssi",
        'movement_counter',
        'tx_power',
        'measurement_sequence_number'
]

class CsvAdapter(BaseAdapter):
    """
    A connection adapter for Influx DB
    """
    def __init__(self, config):
        self.CSV_FOLDER = config.get('CSV_FOLDER')
        self.TIMESERIES_NAME = config.get('TIMESERIES_NAME')

    def is_ready(self):
        return self.CSV_FOLDER and self.TIMESERIES_NAME

    def connect(self):
        # TO DO - PROTECT AGAINS TRAVERSE
        file_name = os.path.join(
            "/",
            self.CSV_FOLDER,
            datetime.today().strftime('%Y%m%d')+".csv"
            )

        if os.path.isfile(file_name):
            logger.debug("Opening file %s" % file_name)
            self.file = open(file_name, 'a', newline='')
            self.writer = csv.DictWriter(self.file, fieldnames=FILED_NAMES)
        else:
            logger.debug("Creating file and writing headers %s" % file_name)
            self.file = open(file_name, 'w+', newline='')
            self.writer = csv.DictWriter(self.file, fieldnames=FILED_NAMES)
            self.writer.writeheader()

    def disconnect(self):
        self.file.close()

    def datapoint_to_csv_dict(self, datapoint):

        data_dict = {}
        data_dict["timestamp"] = datapoint.timestamp
        data_dict.update(datapoint.tag_data)
        data_dict.update(datapoint.sensor_data)
        return data_dict

    def push_metrics(self, metrics):
        logger.info("Pushing metrics to CSV")
        datapoints_dict = [
            self.datapoint_to_csv_dict(metric) for metric in metrics
        ]
        for point in datapoints_dict:
            self.writer.writerow(point)

    def connect_and_push_metrics(self, metrics):
        self.connect()
        self.push_metrics(metrics)
        self.disconnect()