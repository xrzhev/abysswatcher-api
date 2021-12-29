from pydantic import BaseModel, Field


class Notice(BaseModel):
    id: int
    domain: str = Field(None, example="www.example.com", description="Domain Name")
    port: int = Field(None, example=443, description="Port Number")
    expire_time: str = Field(None, example="2038-01-19 03:14:07", description="Expire SSLCert time")
    cert_state: str = Field(None, example="Fine", description="""
        SSL Certificate state
        * Expire_left_days >= 30: Fine
        * Expire_left_days > 15 : Warning
        * Expire_left_days > 7  : Danger
        * Expire_left_days <= 0 : Expired
    """)
    update_check_time: str = Field(None, example="2038-01-19 00:00:00", description="Cert Last Check Time")

    class Config:
        orm_mode = True