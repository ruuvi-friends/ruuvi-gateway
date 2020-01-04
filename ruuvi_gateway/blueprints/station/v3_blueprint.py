from datetime import datetime
from ruuvi_gateway.utils import logger
from flask import Blueprint, abort, request, current_app as app
from ruuvi_gateway import RuuviDatapoint, RuuviGateway

SUPPORTED_TAG_VERSIONS = [3, 5]

v3_blueprint = Blueprint('v3_blueprint', __name__)

@v3_blueprint.route('/push', methods=['POST'])
def push():
    # See tests/fixtures.py to see what are the data
    request_json = request.json
    measurements = []

    if not request_json or 'deviceId' not in request_json:
        abort(400)

    recieved_at = None

    sender_data = {
        "device_id": request_json['deviceId'],
        "battery_level": request_json['batteryLevel'],
        'location': request_json.get('location', {})
    }

    logger.debug("Processing data from %s" % sender_data['device_id'])
    
    for tag in request.json['tags']:
        if tag['dataFormat'] not in SUPPORTED_TAG_VERSIONS:
            logger.warning("TAG WITH UNSUPPORTED DATA VERSION - IGNORING")
            continue

        logger.debug("Processing tag data of version %s" % tag['dataFormat'])

        tag_iso_date = tag['updateAt']

        # 'accelX': 0.478,
        # 'accelY': -0.835,
        # 'accelZ': -0.006,
        # 'dataFormat': 3,
        # 'defaultBackground': 0,
        # 'favorite': True,
        # 'humidity': 61.5,
        # 'id': 'E2:F7:D6:64:DE:42',
        # 'measurementSequenceNumber': 0,
        # 'movementCounter': 0,
        # 'name': 'Discovery One',
        # 'pressure': 972.54,
        # 'rawDataBlob': None, # BLOB
        # 'rssi': -62,
        # 'temperature': 4.52,
        # 'txPower': 0.0,
        # 'updateAt': '2020-01-04T13:31:43+0200',
        # 'voltage': 3.193

        sensor_data = {
            "humidity": tag.get('humidity', None),
            "pressure": tag.get('pressure', None),
            "temperature": tag.get('temperature', None),
            "accel_x": tag.get('accelX', None),
            "accel_y": tag.get('accelY', None),
            "accel_z": tag.get('accelZ', None),
            "voltage": tag.get('voltage', None),
            "rssi": tag.get('rssi', None),
            'movement_counter': tag.get('movementCounter', None),
            'tx_power': tag.get('txPower', None),
            'measurement_sequence_number': tag.get('measurementSequenceNumber', None),
        }

        tag_data = {
            "tag_id": tag['id'],
            "name": tag.get('name', None),
            "favorite": tag.get('favorite', None)
        }

        measurements.append(
            RuuviDatapoint(tag_iso_date, tag_data, sender_data, sensor_data)
            )
    RuuviGateway(app.config).dispatch(measurements)

    return ('OK', 200)
