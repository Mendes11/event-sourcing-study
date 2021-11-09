from enum import Enum
from uuid import UUID

from models import BaseModel


class InputTypes(str, Enum):
    continuous = 'continuous'
    categoric = 'categoric'
    timestamp = 'timestamp'


class DeviceInput(BaseModel):
    device_id: UUID
    name: str
    input_type: InputTypes

    class Config:
        use_enum_values = True