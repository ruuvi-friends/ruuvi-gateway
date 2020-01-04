
[![Build Status](https://travis-ci.org/sergioisidoro/ruuvi-gateway.svg?branch=master)](https://travis-ci.org/sergioisidoro/ruuvi-gateway)  [![codecov](https://codecov.io/gh/sergioisidoro/ruuvi-gateway/branch/master/graph/badge.svg)](https://codecov.io/gh/sergioisidoro/ruuvi-gateway)


# Ruuvi 🔩 gateway 🚪
A simple flask server to relay data from the ruuvi station

## Intro
Ruuvi tags have a [neat app](https://github.com/ruuvi/com.ruuvi.station) that accesses the data of your ruuvi sensors. However the app does not have long term persistence, and you don't have any easy way to export long term data.

The app has, however, support for a gateway, that sends data as POST request to a server. -- The docs can be found [here](https://github.com/ruuvi/com.ruuvi.station/wiki)

This project acts as that gateway to push data to databases 

## Currently supported backends
* InfluxDb


# Starting

0. Change the configs or provide them them in the docker env
1. Deploy the app somewhere
2. Use `<your_server_address>/station/v3/push` in the Ruuvi station app

## Authorization 
**CURRENTLY NOT SUPPORTED! - see [issue in app repo](https://github.com/ruuvi/com.ruuvi.station/issues/83)**

You might not want to have a server that anyone can push things into.
You can add a layer of authentication through the settings 

```
BASIC_AUTH_FORCE=True
BASIC_AUTH_USERNAME='user'
BASIC_AUTH_PASSWORD='pass'
```

After that you should add those to your Ruuvi mobile app gateway address like: `https://user:pass@<yourserver>/station/v3/push`

## CSV Adapter
This is the simplest of use cases, which is to dump all the data to a CSV file.
All you need to do is set the env variable: `CSV_FOLDER` with the folder (eg. `/User/you/Desktop`)

To keep the files from growing forever, there will be one file per day:
```
├── CSV_FOLDER/
│   ├── 20200101.csv
│   ├── 20200102.csv
│   ├── 20200103.csv
│   └── ...
```

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
docker run -p 8086:8086 --network ruuvi-influx --name influxdb influxdb
docker run -p 8888:8888 --network ruuvi-influx chronograf
```

2. Run the ruuvi-gateway:
    
    *  Using docker
        - Change the configurations (see configs section)
        - `docker build -t ruuvig-gateway .` 
        - `docker run -p 5000:5000 -v --env-file docker_env.env --network ruuvi-influx ruuvig-gateway` 
        - OR
        - `docker run -p 5000:5000 -v $(pwd)/instance:/app/instance --network ruuvi-influx ruuvi-gateway`

    * Or Using your local environment
        - Change the configurations in `instance/config.py`
        - pipenv install 
        - pipenv run `pipenv run flask run --host=0.0.0.0`

3. When accessing chronograf on localhost:9092, you should also configure it with the influxdb address `influxdb:8086`

4. You should start seeing data coming in

## Configurations and deployment

Notes about Docker
It's a bad practice to include the configurations inside the docker image. Especially if they contain secrets. To mitigate this you can either use env variables for the configuration, or you can map the `instance` folder into the docker container. Runing the container without any configurations will possibly result in the message `NO GATEWAYS ARE CONFIGURED!`. Your options are:

- Give variables via docker run / docker compose, et

       `docker run -p 5000:5000 --env-file docker_env.env ...... ` 

       `docker run -p 5000:5000 --env INFLUX_DB_NAME=ruuvi --env INFLUX_URL=influxdb .....`


- Map the instance folder (that is not originally in the image) which will override the defaults

A production ready image is published in sergioisidoro/ruuvi-gateway in [docker hub](https://hub.docker.com/r/sergioisidoro/ruuvi-gateway)


# Contributing.

To add a new adapter, you should implement the methods `is_ready`, and `connect_and_push_metrics`. 
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

To see data, and add test cases, head over to /tests/fixtures.py


## 🥳 Authors
* [Sergio Isidoro](www.sergioisidoro.com)
* (Your name here)
