from pydantic import BaseModel
from typing import List


class RabbitMessage(BaseModel):
    name: str
    carModels: str
    gasStation: int
    indexes: int
    sails: int
    recommendations: List[str]
