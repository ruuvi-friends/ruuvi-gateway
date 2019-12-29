from datetime import datetime
from ruuvi_gateway.utils import logger
from flask import Blueprint, abort, request, current_app as app
from ruuvi_gateway import RuuviDatapoint, RuuviGateway

DATA_VERSION = 3

v3_blueprint = Blueprint('v3_blueprint', __name__)

@v3_blueprint.route('/push', methods=['POST'])
def push():
    """
    {'tags': [
        {
            'accelX': -0.012, 
            'accelY': -0.02, 
            'accelZ': 0.999, 
            'dataFormat': 3, 
            'defaultBackground': 2, 
            'favorite': True, 
            'humidity': 75.5, 
            'id': 'CD:81:78:21:E0:81', 
            'measurementSequenceNumber': 0, 
            'movementCounter': 0, 
            'name': 'Balcony', 
            'pressure': 1012.1, 
            'rssi': -78, 
            'temperature': 3.35, 
            'txPower': 0.0, 
            'updateAt': '2019-12-29T19:07:40+0200', 
            'voltage': 3.043
            }
        ], 
    'batteryLevel': 90, 
    'deviceId': '97aed60e-51ea-490e-bfb9-eeded650f845', 
    'eventId': '812d23e5-d20a-4fae-a438-cacfadbf63f9', 
    'location': 
        {
            'accuracy': 2000.0, 
            'latitude': 60.288288288288285, 
            'longitude': 25.047432133734535}, 
            'time': '2019-12-29T19:07:40+0200'
        }
    """
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

    logger.info("Processing data from %s" % sender_data['device_id'])

    for tag in request.json['tags']:

        if tag['dataFormat'] != DATA_VERSION:
            logger.warning("TAG WITH INCORRECT DATA VERSION - IGNORING")
            continue
                
        tag_iso_date = tag['updateAt']
        
        sensor_data = {
            "humidity": tag['humidity'],
            "pressure": tag['pressure'],    
            "temperature": tag['temperature'],
            "accelX": tag['accelX'],
            "accelY": tag['accelY'],
            "accelZ": tag['accelZ'],
            "voltage": tag['voltage'],
            "rssi": tag['rssi'],
            'movement_counter': tag['movementCounter'], 
            'tx_power': tag['txPower'] 
        }

        tag_data = {
            "tag_id": tag['id'],
            "name": tag['name'],
            "favorite": tag['favorite']
        }

        measurements.append(
            RuuviDatapoint(tag_iso_date, tag_data, sender_data, sensor_data)
            )

        RuuviGateway(app.config).dispatch(measurements)

    return ('', 200)
