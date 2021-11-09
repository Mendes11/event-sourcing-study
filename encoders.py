from datetime import datetime
from json.encoder import JSONEncoder
from typing import Any
from uuid import UUID


class ExtendedJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return o.timestamp()
        elif isinstance(o, UUID):
            return str(o)
