# Devices Service - Events Sourcing Case Study


This project aims to experiment with the concepts of Events Sourcing, where 
we use the Event Store as our source of truth.

The selected Event Store is Kafka, since it is successfully used in 
multiple architectures consisting of this pattern.


## Devices Service

The devices service is an IOT service where users can manage Devices and 
their Inputs `(Device Inputs)`.

Operations are normal CRUD operations:

* Create Device
* Get Devices (Listing)
* Get Device (Retrieve)
* Update Device
* Delete Device

Since this API works with events, each user operation will in turn generate 
a specific event, which in turn, will be read from a separate thread, where 
it processes the event log and generate a current state of each device from it.

Therefore, this API works with the concept of `Eventual Consistency`, where 
you may not read your writes right they were written.


## Important Note

> Since this example doesn't deal with sharing data through partitions, we 
cannot scale it (maximum number of concurrent services should be 1) and 
therefore 1 partition in Kafka, otherwise the API will return only the data 
whose keys are on the specific partitions it is connected to.

## Usage

To use, you must first configure the environment variables:

```
KAFKA_BOOSTRAP_SERVERS: List of Kafka clusters to connect to. (Csv like)
DEVICES_TOPIC: Name of the devices events topic <default: devices>
DEVICES_INPUT_TOPIC: Name of the devices inputs topic <default: device_inputs>
CONSUMER_GROUP_ID: The ID of this consumer group for all registered topics 
<default: new_devices_service>
```


Then, call it in a virtual environment with python 3.7 or above:

`python main.py`

This will start an API at port 8000

## OpenAPI Schema
Since we are using FastAPI, we automatically have an OpenAPI documentation

### Swagger

`<host>/docs`

### Redoc

`<host>/redoc`
