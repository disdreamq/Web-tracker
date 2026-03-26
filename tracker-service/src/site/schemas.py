from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class SSiteCreate(BaseModel):
    url: HttpUrl
    hash: str

class SSiteDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    hash: str
    created_at: datetime
    updated_at: datetime
