from datetime import datetime
from ruuvi_gateway.utils import logger
from flask import Blueprint, abort, request, current_app as app
from ruuvi_gateway import RuuviDatapoint, RuuviGateway

v1_blueprint = Blueprint('v1_blueprint', __name__)

@v1_blueprint.route('/push', methods=['POST'])
def push():
    """
        Expected data
        { deviceId: 'laurin-s8',
          eventId: '591db9bc-32f0-4059-86e0-8e6cc808492c',
          tags: 
           [ { accelX: 0.019,
               accelY: -0.003,
               accelZ: 1.041,
               defaultBackground: 0,
               favorite: false,
               humidity: 88,
               id: 'F8:AC:76:59:5B:24',
               name: 'Over Humidity',
               pressure: 974.01,
               rawDataBlob: [Object],
               rssi: -45,
               temperature: 27.25,
               updateAt: 'Mar 6, 2018 11:21:46',
               voltage: 2.989 } ],
          time: 'Mar 6, 2018 11:21:46' }
    """

    request_json = request.json
    measurements = []

    if not request_json or 'deviceId' not in request_json:
        abort(400)

    recieved_at = datetime.strptime(
        request_json['updateAt'], "%b %-d, %Y %H:%m:S"
    ).isoformat()

    sender_data = {
        "device_id": request_json['deviceId']
    }
    
    logger.info("Processing data from %s" % sender_data['device_id'])
    
    for tag in request.json['tags']:
        
        tag_iso_date = datetime.strptime(
            tag['updateAt'], "%b %-d, %Y %H:%m:S"
            ).isoformat()

        sensor_data = {
            "humidity": tag['humidity'],
            "pressure": tag['pressure'],    
            "temperature": tag['temperature'],
            "accelX": tag['accelX'],
            "accelY": tag['accelY'],
            "accelZ": tag['accelZ'],
            "voltage": tag['voltage'],
            "rssi": tag['rssi']
        }

        tag_data = {
            "tag_id": tag['id'],
            "name": tag['name'],
        }

        measurements.append(
            RuuviDatapoint(tag_iso_date, tag_data, sender_data, sensor_data)
            )

        RuuviGateway.new(app.config).dispatch(measurements)

        return ('', 204)
