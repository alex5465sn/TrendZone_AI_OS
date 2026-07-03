from pydantic import BaseModel


class SystemInfoBase(BaseModel):
    app_name: str
    version: str


class SystemInfoCreate(SystemInfoBase):
    pass


class SystemInfoResponse(SystemInfoBase):
    id: int

    model_config = {
        "from_attributes": True
    }