import os
import tempfile
import unittest
import ruuvi_gateway
from ruuvi_gateway.adapters.csv_adapter import CsvAdapter
from .fixtures import (
    fixture_sender_data,
    fixture_sensor_data,
    fixture_tag_data,
    fixture_tag_iso_date
    )

class CsvAdapterBaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = ruuvi_gateway.create_app()
        self.app.config['TESTING'] = True
        self.app.config['CSV_FOLDER'] = tempfile.mkdtemp()
        self.app.testing = True
        self.testing_app = self.app.test_client()

    def tearDown(self):
        pass
        # os.unlink(self.app.config['CSV_FOLDER'])

    def test_readyness(self):
        """Start with a blank database."""
        adapter = CsvAdapter(self.app.config)
        assert adapter.is_ready()

    def test_non_readyness(self):
        """Start with a blank database."""
        self.app.config['CSV_FOLDER'] = None
        adapter = CsvAdapter(self.app.config)
        assert not adapter.is_ready()
