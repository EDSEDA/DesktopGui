from typing import List

from pydantic import BaseModel


class RabbitMessage(BaseModel):
    name: str
    carModels: str
    gasStation: int
    indexes: int
    sails: int
    recommendations: List[str]
