import json
import uuid
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel as Model

from encoders import ExtendedJSONEncoder


class BaseModel(Model):
    id: UUID = None
    created_at: datetime = None
    updated_at: datetime = None
    deleted_at: datetime = None
    deleted: bool = False

    def bytes(self) -> bytes:
        d = self.dict()
        d['id'] = str(d['id'])
        return json.dumps(d, cls=ExtendedJSONEncoder).encode('utf-8')

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls(**json.loads(data.decode('utf-8')))

    @classmethod
    def new(cls, **kwargs):
        # FIXME This is a bad design, due to the ID not being guaranteed of
        #  being unique (even though i'm using UUIDs, if it was integers the
        #  only way to work would be if this is a single process/thread
        #  application, with no concurrency)
        model_id = uuid.uuid4()
        return cls(
            **kwargs, id=model_id,
            created_at=datetime.utcnow().timestamp(),
            updated_at=datetime.utcnow().timestamp()
        )

    def update(self, **kwargs):
        for name, value in kwargs.items():
            if not hasattr(self, name):
                raise ValueError(f"{name} is not a field of {type(self)}")
            setattr(self, name, value)
        self.updated_at = datetime.utcnow().timestamp()

    def set_to_delete(self):
        self.deleted = True
        self.deleted_at = datetime.utcnow().timestamp()
        self.updated_at = datetime.utcnow().timestamp()
        return self


class BaseAPIModel(Model):
    id: UUID = None
    created_at: datetime = None
    updated_at: datetime = None