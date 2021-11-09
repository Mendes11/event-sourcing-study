from copy import deepcopy
from typing import Dict
from uuid import UUID

from confluent_kafka import Message

from models.device_input import DeviceInput
from models.device import Device


class DB:
    """
    Represents a Database Instance.

    ### STUDY NOTE
    If we want to materialize some resources from external events
    of a stream that has multiple partitions and this service will have
    multiple consumers of the same group_id, then we will need to persist
    this Database's data in a real one, since each consumer will be linked
    to a specific partition and therefore this class wouldn't have the
    entire resources, just those related to specific keys...

    Unless this is desirable (ie: we will only work with the same keys only)
    we need to either have an unique group_id per consumer of the event
    stream, or to use the external DB mentioned above.

    """
    def __init__(self):
        """
        Set our "tables" which is a map of key/value where the key is the
        object ID and the value is the last object received from the stream
        (already deserialized) for that ID.
        """
        self._devices: Dict[UUID, Device] = {}
        self._inputs: Dict[UUID, DeviceInput] = {}
        self._deleted_devices: Dict[UUID, Device] = {}
        self._deleted_inputs: Dict[UUID, Device] = {}

    @property
    def devices(self):
        return deepcopy(self._devices)

    @property
    def device_inputs(self):
        return deepcopy(self._inputs)

    def new_model_event(self, obj, storage, deleted_storage):
        """
        Check if the received object is a new one or already exists.

        If it exists, we ensure the updated_at field is higher than the
        current stored to prevent late events from overriding the values.

        If the object is deleted, we then remove it from the storage table
        and move it to deleted_storage.

        :param obj:
        :param storage:
        :param deleted_storage:
        :return:
        """
        if obj.id not in storage and not obj.deleted:
            storage[obj.id] = obj
        elif obj.id in storage and obj.updated_at > storage[obj.id].updated_at:
            storage[obj.id] = obj
            if obj.deleted:
                del storage[obj.id]
                deleted_storage[obj.id] = obj
                print(f"{obj} was deleted!")

    def new_device_event(self, evt: Message):
        print(f"New Device Event - Offset: {evt.offset()}")
        device = Device.from_bytes(evt.value())
        self.new_model_event(device, self._devices, self._deleted_devices)

    def new_input_event(self, evt: Message):
        ipt = DeviceInput.from_bytes(evt.value())
        self.new_model_event(ipt, self._inputs, self._deleted_inputs)

db: DB = None

def get_db():
    global db

    if db is None:
        db = DB()
    return db
