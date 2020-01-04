import os
import tempfile
import unittest
import ruuvi_gateway
from ruuvi_gateway.adapters.influxdb_adapter import InfluxAdapter
from .fixtures import (
    fixture_sender_data,
    fixture_sensor_data,
    fixture_tag_data,
    fixture_tag_iso_date
    )

class InfluxAdapterBaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = ruuvi_gateway.create_app()
        self.app.config['TESTING'] = True
        self.app.config['INFLUX_DB_NAME'] = "ruuvi"
        self.app.testing = True
        self.testing_app = self.app.test_client()

    def tearDown(self):
        pass
        # os.unlink(self.app.config['CSV_FOLDER'])

    def test_readyness(self):
        """Start with a blank database."""
        adapter = InfluxAdapter(self.app.config)
        assert adapter.is_ready()

    def test_non_readyness(self):
        """Start with a blank database."""
        self.app.config['INFLUX_DB_NAME'] = None
        adapter = InfluxAdapter(self.app.config)
        assert not adapter.is_ready()
