from datetime import datetime

from pydantic import BaseModel


class BuildLogEntry(BaseModel):
    id: str
    timestamp: datetime
    step: str
    title: str
    description: str

    class Config:
        from_attributes = True
