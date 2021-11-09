import time
from collections import defaultdict
from threading import Thread
from typing import List

from confluent_kafka import Consumer as ConfluentConsumer, Message, \
    TopicPartition, OFFSET_BEGINNING, OFFSET_INVALID, KafkaException

from db import get_db
from settings import KAFKA_BOOSTRAP_SERVERS, CONSUMER_GROUP_ID, \
    DEVICES_TOPIC, DEVICES_INPUT_TOPIC


class Consumer:
    def __init__(self, config, messages_batch=5):
        self.canceled = False
        self._consumer = ConfluentConsumer(config)
        self.messages_batch = messages_batch
        self.subscriptions = defaultdict(set) # Event, Targets
        self.thread = Thread(target=self._consume, daemon=True)
        self.ready = False
        self.partitions_watermark = {}
        self.partitions = []


    def _notify_subscriptions(self, message: Message):
        if message.topic() in self.subscriptions:
            for callback in self.subscriptions[message.topic()]:
                callback(message)

    def _on_assign(self, consumer, partitions: List[TopicPartition]):
        for p in partitions:
            if p not in self.partitions:
                print(f"Assigning '{p}' to Offset BEGINNING")
                p.offset = OFFSET_BEGINNING

        consumer.assign(partitions)
        self.partitions = self._consumer.position(partitions)
        for p in self.partitions:
            self.partitions_watermark[
                p] = self._consumer.get_watermark_offsets(p)

    def check_ready(self):
        self.partitions = self._consumer.position(self.partitions)
        if not self.partitions or any(
                p.offset != OFFSET_INVALID and p.offset < self.partitions_watermark[p][1] for p in self.partitions):
            self.ready = False
        else:
            self.ready = True

    def _consume(self):
        while not self.canceled:
            msgs = self._consumer.consume(
                num_messages=self.messages_batch, timeout=.1)
            for msg in msgs:
                if msg.error():
                    raise KafkaException(msg.error())
                self._notify_subscriptions(msg)
            if not self.ready:
                self.check_ready()

    def add_subscription(self, topic, callback):
        self.subscriptions[topic].add(callback)

    def start(self):
        self._consumer.subscribe(
            list(self.subscriptions.keys()), on_assign=self._on_assign
        )
        self.thread.start()
        while not self.ready:
            time.sleep(.2)

    def close(self):
        self._consumer.unsubscribe()
        self._consumer.close()
        self.canceled = True
        self.thread.join()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


consumer: Consumer = None

def start_consumer():
    print("Starting Consumer")
    global consumer
    db = get_db()
    if consumer is None:
        consumer = Consumer({
            'bootstrap.servers': KAFKA_BOOSTRAP_SERVERS,
            'group.id': CONSUMER_GROUP_ID,
            'auto.offset.reset': 'earliest'
        })

    consumer.add_subscription(DEVICES_TOPIC, db.new_device_event)
    consumer.add_subscription(DEVICES_INPUT_TOPIC, db.new_input_event)
    consumer.start()
    return consumer
