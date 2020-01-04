import os
import unittest
import ruuvi_gateway
from .fixtures import (
    mobile_app_request,
    empty_mobile_app_request,
    mobile_app_v5_request,
    mobile_app_v3_request
    )

class RuuviStationBaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = ruuvi_gateway.create_app()
        self.app.testing = True
        self.testing_app = self.app.test_client()

    def tearDown(self):
        pass

    def test_heartbeat_request(self):
        """Start with a blank database."""
        response = self.testing_app.get('/heartbeat')
        assert b"Yes, everything's fine mate!" in response.data

    def test_empty_mobile_post_request(self):
        """Start with a blank database."""
        response = self.testing_app.post(
            'station/v3/push',
            json=empty_mobile_app_request
        )
        assert b"OK" in response.data

    def test_v3_mobile_post_request(self):
        """Start with a blank database."""
        response = self.testing_app.post(
            'station/v3/push',
            json=mobile_app_v3_request
        )
        assert b"OK" in response.data

    def test_v5_mobile_post_request(self):
        """Start with a blank database."""
        response = self.testing_app.post(
            'station/v3/push',
            json=mobile_app_v5_request
        )
        assert b"OK" in response.data

    def test_v3_and_v5_mobile_post_request(self):
        """Start with a blank database."""
        response = self.testing_app.post(
            'station/v3/push',
            json=mobile_app_request
        )
        assert b"OK" in response.data
