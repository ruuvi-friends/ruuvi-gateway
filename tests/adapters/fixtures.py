import copy

fixture_tag_iso_date = '2020-01-04T13:31:43+0200'

fixture_sender_data = {
    'deviceId': '97aed60e-51ea-490e-bfb9-eeded650f845',
    'eventId': '7a1ca469-2101-42b4-8289-2359490860d9',
    'location': {
        'accuracy': 2000.0,
        'latitude': 60.392296713513516,
        'longitude': 25.664867312888995
    }
}

fixture_sensor_data = {
    "humidity": 50,
    "pressure": 972.54,
    "temperature": 4.52,
    'accel_x': 0.478,
    'accel_y': -0.835,
    'accel_z': -0.006,
    "voltage": 3.193,
    "rssi": -62,
    'movement_counter': 0,
    'tx_power': 0.0,
    'measurement_sequence_number': 0
}

fixture_tag_data = {
    "tag_id": 'E2:F7:D6:64:DE:42',
    "name": 'Discovery One',
    "favorite": True
}