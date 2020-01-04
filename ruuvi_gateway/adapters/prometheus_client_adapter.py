import os
from flask import current_app as app
from ruuvi_gateway.utils import logger
from ruuvi_gateway.adapters import BaseAdapter
from ruuvi_gateway.datapoint import RuuviDatapoint
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import Gauge, make_wsgi_app, Summary

RUUVI_DATA = Gauge(
    'ruuvi_sensors', 'Ruuvi sensor data',
    ['tag_id', 'fields']
)

class PrometheusClientAdapter(BaseAdapter):
    """
    Prometheus client exposes the CURRENT state of the sensors to a page,
    where a prometheus server can go get metrics from.
    """

    def __init__(self, config):
        # Prometheus only uses snake case
        self.PROMETHEUS_CLIENT_ENDPOINT = config.get('PROMETHEUS_CLIENT_ENDPOINT')

    def is_ready(self):
        return self.PROMETHEUS_CLIENT_ENDPOINT

    def connect(self):
        self.app_dispatch = DispatcherMiddleware(app, {
            "/prometheus": make_wsgi_app()
        })

    def push_metrics(self, metrics):
        logger.info("Exposing latest metrics in Prometheus client")

        sorted_list = RuuviDatapoint.sort_datapoint_list(metrics)
        grouped_list = RuuviDatapoint.group_by_tagid(sorted_list)

        for tag_id, datapoints in grouped_list.items():
            print(datapoints[0].sensor_data)
            for metric, value in datapoints[0].sensor_data.items():
                RUUVI_DATA.labels(tag_id, metric).set(value)

    def connect_and_push_metrics(self, metrics):
        self.connect()
        self.push_metrics(metrics)