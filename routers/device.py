from uuid import UUID

from fastapi import APIRouter
from starlette.responses import Response

from consumers import get_db
from exceptions import NotFound
from controllers.device import new_device_event, update_device_event
from models.device import APIDevice, DeviceForm, ListDevicesResponse

router = APIRouter(
    prefix="/api/v1/devices",
    tags=["devices"]
)


@router.post("/", response_model=APIDevice)
async def create_device(device: DeviceForm):
    created_device = await new_device_event(device)
    return APIDevice(**created_device.dict())


@router.get("/", response_model=ListDevicesResponse)
async def get_devices():
    db = get_db()
    return ListDevicesResponse(items=[
        APIDevice(**device.dict())  for device in db.devices.values()
    ])


@router.get("/{id}/", response_model=APIDevice)
async def get_device(id: UUID):
    db = get_db()
    return APIDevice(**db.devices[id].dict())


@router.put("/{id}/", response_model=APIDevice)
async def update_device(id: UUID, data: DeviceForm):
    db = get_db()
    try:
        device = db.devices[id]
    except KeyError:
        raise NotFound()
    device.update(**data.dict())
    await update_device_event(device)
    return APIDevice(**device.dict())


@router.delete("/{id}/")
async def delete_device(id: UUID):
    db = get_db()
    try:
        device = db.devices[id]
    except KeyError:
        raise NotFound()

    device.set_to_delete()
    await update_device_event(device)
    return Response(status_code=204)
