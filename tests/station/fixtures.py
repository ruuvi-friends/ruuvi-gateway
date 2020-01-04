empty_mobile_app_request = {
    'batteryLevel': 16,
    'deviceId': '97aed60e-51ea-490e-bfb9-eeded650f845',
    'eventId': '7a1ca469-2101-42b4-8289-2359490860d9',
    'location': {
        'accuracy': 2000.0,
        'latitude': 60.392296713513516,
        'longitude': 25.664867312888995
    },
    'tags': [],
    'time': '2020-01-04T13:45:13+0200'
}

version_5_tag = {
    'accelX': -0.836,
    'accelY': -0.34,
    'accelZ': 0.532,
    'dataFormat': 5,
    'defaultBackground': 3,
    'favorite': True,
    'humidity': 30.17,
    'id': 'F9:6C:55:27:C4:6E',
    'measurementSequenceNumber': 30464,
    'movementCounter': 123,
    'name': 'Pod bay',
    'pressure': 971.35,
    'rawDataBlob': None, # BLOB
    'rssi': -79,
    'temperature': 24.92,
    'txPower': 4.0,
    'updateAt': '2020-01-04T13:31:43+0200',
    'voltage': 3.187
}

version_3_tag = {
    'accelX': 0.478,
    'accelY': -0.835,
    'accelZ': -0.006,
    'dataFormat': 3,
    'defaultBackground': 0,
    'favorite': True,
    'humidity': 61.5,
    'id': 'E2:F7:D6:64:DE:42',
    'measurementSequenceNumber': 0,
    'movementCounter': 0,
    'name': 'Discovery One',
    'pressure': 972.54,
    'rawDataBlob': None, # BLOB
    'rssi': -62,
    'temperature': 4.52,
    'txPower': 0.0,
    'updateAt': '2020-01-04T13:31:43+0200',
    'voltage': 3.193
}

mobile_app_v3_request = empty_mobile_app_request
mobile_app_v3_request['tags'] = [version_3_tag]

mobile_app_v5_request = empty_mobile_app_request
mobile_app_v5_request['tags'] = [version_5_tag]

mobile_app_request = empty_mobile_app_request
mobile_app_request['tags'] = [version_5_tag, version_3_tag]
