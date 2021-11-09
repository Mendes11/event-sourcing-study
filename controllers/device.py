from db import get_db
from models.device import Device
from producers import async_produce
from settings import DEVICES_TOPIC


async def new_device_event(device: Device):
    # TODO Check ID before sending the event
    device = Device.new(name=device.name, description=device.description)
    db = get_db()

    # FIXME This problem is the same as the one in BaseModel, regarding how
    #  to guarantee the ID is not duplicated. In here we are dealing with
    #  eventual consistence due to the fact of our DB instance being
    #  internal to this process (it just has the latest logs for each key)
    while db.devices.get(device.id) is not None:
        device = Device.new(name=device.name, description=device.description)

    await async_produce(DEVICES_TOPIC, device.bytes(), str(device.id))
    return device


async def update_device_event(device: Device):
    await async_produce(
        DEVICES_TOPIC, device.bytes(), key=str(device.id)
    )
    return device
