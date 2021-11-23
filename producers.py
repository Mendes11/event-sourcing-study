import asyncio
from concurrent.futures import Executor
from threading import Thread

import confluent_kafka
from confluent_kafka import KafkaException

from settings import KAFKA_BOOTSRAP_SERVERS


class Producer:
    def __init__(self, configs, executor: Executor):
        self._producer = confluent_kafka.Producer(configs)
        self._cancelled = False
        self.executor = executor

    def start(self):
        self._pool_task = self.executor.submit(self._poll_loop)

    def _poll_loop(self):
        print("Starting Producer Pool Loop")
        while not self._cancelled:
            self._producer.poll(0.1)
        print("Producer Loop Stopped")

    def close(self):
        print("Shutting Down Producer")
        self._cancelled = True
        self._pool_task.result(2)

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

def start_producer(executor):
    global producer

    if producer is None:
        producer = Producer({'bootstrap.servers': KAFKA_BOOTSRAP_SERVERS,}, executor)
        producer.start()
    return producer

def stop_producer():
    if producer is not None:
        producer.close()
