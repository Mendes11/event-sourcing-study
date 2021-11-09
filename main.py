from concurrent.futures import ThreadPoolExecutor

import uvicorn
from fastapi import FastAPI
from consumers import start_consumer, stop_consumer
from producers import start_producer, stop_producer
from routers import device

app = FastAPI()

app.include_router(device.router)


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as executor:
        start_producer(executor)
        start_consumer(executor)
        uvicorn.run(app)
        stop_consumer()
        stop_producer()
