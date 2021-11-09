from typing import List

from pydantic import BaseModel as Model

from models import BaseAPIModel, BaseModel


class DeviceData(Model):
    """
    Base Attributes of a Device
    """
    name: str
    description: str


class DeviceForm(DeviceData):
    """
    Model to be used as Input for Devices
    """
    ...


class APIDevice(DeviceData, BaseAPIModel):
    """
    Model to be used as Output for Devices
    """
    ...


class Device(DeviceData, BaseModel):
    """
    Model to be used internally to generate the events
    """


class ListDevicesResponse(Model):
    items: List[APIDevice]


