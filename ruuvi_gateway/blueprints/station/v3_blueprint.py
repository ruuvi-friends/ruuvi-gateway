from datetime import datetime
import pprint
from ruuvi_gateway.utils import logger
from flask import Blueprint, abort, request, current_app as app
from ruuvi_gateway import RuuviDatapoint, RuuviGateway

SUPPORTED_TAG_VERSIONS = [3, 5]

pp = pprint.PrettyPrinter(indent=4)
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

        logger.info("Processing tag data of version %s" % tag['dataFormat'])

        tag_iso_date = tag['updateAt']

        sensor_data = {
            "humidity": tag.get('humidity', None),
            "pressure": tag.get('pressure', None),
            "temperature": tag.get('temperature', None),
            "accelX": tag.get('accelX', None),
            "accelY": tag.get('accelY', None),
            "accelZ": tag.get('accelZ', None),
            "voltage": tag.get('voltage', None),
            "rssi": tag.get('rssi', None),
            'movement_counter': tag.get('movementCounter', None),
            'tx_power': tag.get('txPower', None)
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
