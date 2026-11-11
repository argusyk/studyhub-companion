from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LabOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    number: int
    title: str
    deadline: datetime
    max_score: int
