import asyncio
from threading import Thread

import confluent_kafka
from confluent_kafka import KafkaException

from settings import KAFKA_BOOSTRAP_SERVERS


class Producer:
    def __init__(self, configs):
        self._producer = confluent_kafka.Producer(configs)
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop, daemon=True)
        self._poll_thread.start()

    def _poll_loop(self):
        while not self._cancelled:
            self._producer.poll(0.1)

    def close(self):
        self._cancelled = True
        self._poll_thread.join()

    def produce(self, topic, value, key, on_delivery=None):
        self._producer.produce(
            topic, value, key=key, on_delivery=on_delivery
        )


async def async_produce(topic, value, key):
    loop = asyncio.get_event_loop()
    result = loop.create_future()

    def ack(err, msg):
        if err:
            loop.call_soon_threadsafe(result.set_exception, KafkaException(
                err))
        else:
            loop.call_soon_threadsafe(result.set_result, msg)

    producer.produce(topic, value, key, on_delivery=ack)
    return result


producer: Producer = None

def start_producer():
    global producer

    if producer is None:
        producer = Producer({'bootstrap.servers': KAFKA_BOOSTRAP_SERVERS,})
    return producer
