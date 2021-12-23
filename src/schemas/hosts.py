from pydantic import BaseModel, Field


class HostBase(BaseModel):
    domain: str = Field(None, example="www.example.com", description="Domain Name")


class HostCreate(HostBase):
    pass


class HostCreateResponse(HostBase):
    id: int

    class Config:
        orm_mode = True


class HostRead(HostBase):
    pass


class Host(HostBase):
    id: int

    class Config:
        orm_mode = True