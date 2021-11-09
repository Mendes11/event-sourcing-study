from decouple import config


KAFKA_BOOSTRAP_SERVERS = config('KAFKA_BOOSTRAP_SERVERS')
CONSUMER_GROUP_ID = config('CONSUMER_GROUP_ID', default='devices_service')
DEVICES_TOPIC = config("DEVICES_TOPIC", default='devices')
DEVICES_INPUT_TOPIC = config("DEVICES_INPUT_TOPIC", default="device_inputs")

