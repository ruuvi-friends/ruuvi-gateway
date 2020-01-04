from ruuvi_gateway.utils import logger
from ruuvi_gateway.adapters.influxdb_adapter import InfluxAdapter
from ruuvi_gateway.adapters.csv_adapter import CsvAdapter
class RuuviGateway:
    """
    Instanciate all adapters that are available
    """

    def __init__(self, config):
        influx_adapter = InfluxAdapter(config)
        csv_adapter = CsvAdapter(config)

        self.adapters = [
            influx_adapter,
            csv_adapter
        ]
        self.adapters = list(filter(lambda x: x.is_ready(), self.adapters))
        if len(self.adapters) == 0:
            logger.warning("NO GATEWAYS ARE CONFIGURED!")

    def dispatch(self, datapoint_list):
        for adapter in self.adapters:
            adapter.connect_and_push_metrics(datapoint_list)