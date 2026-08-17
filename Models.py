from pydantic import BaseModel


class HubModel(BaseModel):
    name: str
    x: int
    y: int
    metadata: str
    other_data: None

class ConnectionModel(BaseModel):
    connection: str
    metadata: str
    other_data: None
