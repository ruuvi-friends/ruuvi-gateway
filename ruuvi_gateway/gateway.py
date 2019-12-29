from ruuvi_gateway.utils import logger
from ruuvi_gateway.adapters.influxdb_adapter import InfluxAdapter

class RuuviDatapoint: 
    """
    Encapsulates the data in a standard format in case the API changes
    """
    def __init__(self, iso_timestamp, tag_data, sender_data, sensor_data):
        # Todo JSON validate the data
        self.iso_timestamp = iso_timestamp
        self.tag_data = tag_data
        self.sender_data = sender_data
        self.sensor_data = sensor_data

class RuuviGateway:
    """
    Instaciate all adapters that are available
    """

    def __init__(self, config):
        influx_adapter = InfluxAdapter(config)
        self.adapters = [
            influx_adapter
        ]
        self.adapters = list(filter(lambda x: x.is_ready(), self.adapters))
        if len(self.adapters) == 0:
            logger.warn("NO GATEWAYS ARE CONFIGURED!")

    def dispatch(self, datapoint_list):
        for adapter in self.adapters:
            adapter.connect_and_push_metrics(datapoint_list)