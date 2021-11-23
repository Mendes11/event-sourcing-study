import logging
from concurrent.futures import ThreadPoolExecutor

import uvicorn
from fastapi import FastAPI
from consumers import start_consumer, stop_consumer
from producers import start_producer, stop_producer
from routers import device

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(message)s")

app = FastAPI()

app.include_router(device.router)


if __name__ == "__main__":
    try:
        with ThreadPoolExecutor(max_workers=4) as executor:
            # start_consumer(executor)
            # start_producer(executor)
            uvicorn.run(app, host="0.0.0.0")
    except Exception:
        logger.exception("Exception Raised")
    finally:
        stop_producer()
        stop_consumer()
