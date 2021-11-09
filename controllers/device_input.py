from models.device_input import DeviceInput
from producers import async_produce
from settings import DEVICES_INPUT_TOPIC


async def new_input_event(ipt: DeviceInput):
    # TODO Check ID Before sending the event
    ipt = DeviceInput.new(
        device_id=ipt.device_id, name=ipt.name, input_type=ipt.input_type
    )
    await async_produce(
        DEVICES_INPUT_TOPIC, ipt.bytes(), key=str(ipt.id)
    )
    return ipt


async def update_input_event(ipt: DeviceInput):
    await async_produce(
        DEVICES_INPUT_TOPIC, ipt.bytes(), key=str(ipt.id)
    )
    return ipt