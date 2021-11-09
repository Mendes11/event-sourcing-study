import uvicorn
from fastapi import FastAPI
from consumers import start_consumer, consumer
from producers import start_producer, producer
from routers import device

app = FastAPI()

app.include_router(device.router)

@app.on_event("startup")
async def start_singletons():
    print("starting_singletons")
    start_producer()
    start_consumer()


@app.on_event("shutdown")
def shutdown_event():
    if consumer is not None:
        consumer.close()
    if producer is not None:
        producer.close()


if __name__ == "__main__":
    uvicorn.run(app)
