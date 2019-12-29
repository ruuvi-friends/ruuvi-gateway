
# Ruuvi 🔩 gateway 🚪
A simple flask server to relay data from the ruuvi station


## Intro
Ruuvi tags have a [neat app](https://github.com/ruuvi/com.ruuvi.station) that accesses the data of your ruuvi sensors. However the app does not have long term persistence, and you don't have any easy way to export long term data.

The app has, however, support for a gateway, that sends data as POST request to a server. -- The docs can be found [here](https://github.com/ruuvi/com.ruuvi.station/wiki)

This project acts as that gateway to push data to databases (right now only influxdb supported).


## Basics
0. Change the configs to your needs
1. Deploy the app somewhere
2. Use `<your_server_address>/v3/push` in the Ruuvi station app

## Authorization (NOT CURRENTLY SUPPORTED! see [issue](https://github.com/ruuvi/com.ruuvi.station/issues/83))
You might not want to have a server that anyone can push things into.
You can add a layer of authentication through the settings 

```
BASIC_AUTH_FORCE=True
BASIC_AUTH_USERNAME='user'
BASIC_AUTH_PASSWORD='pass'
```

After that you should add those to your Ruuvi mobile app gateway address like: `https://user:pass@<yourserver>/v3/push`

## InfluxDB support
```
# INFLUXDB PARAMETERS

INFLUX_DB_NAME="ruuvi"  # Mandatory

# INFLUX_URL=           # defaults to 'localhost'
# INFLUX_PORT=          # defaults to 8086
# INFLUX_USER=          # defaults to none
# INFLUX_PASSWORD=      # defaults to none
```

#### Testing things

1. To easily test things you can spin a docker container of influx+kapacitor
```
docker network create -d bridge ruuvi-influx
docker run -p 8086:8086 --name influxdb influxdb
docker run -p 9092:9092 --name kapacitor kapacitor
docker run -p 8888:8888 chronograf
```

2. If you are running in docker, you should configure the ruuvi-gateway with `INFLUX_URL=influxdb`. Otherwise, if you are running the python code locally, the defaults should work


3. When accessing chronograf on localhost:9092, you should also configure it with the influxdb address `influxdb:8086`

4. You should start seeing data coming in

## Contributing.

To add a new adapter, you sould implement the methods `is_ready`, and `connect_and_push_metrics`. 
After that, import your adapter in `gateway.py` and it here:

```
def __init__(self, config):
        your_adapter = YourAdapter(config)
        ...
        self.adapters = [
            influx_adapter
            your_adapter
        ]
```
