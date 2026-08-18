from pydantic import BaseModel, Field


class HubModel(BaseModel):
    name: str = Field(pattern=r"^[^- ]+$")
    x: int
    y: int
    metadata: str
    other_data: None

class ConnectionModel(BaseModel):
    connection: str
    metadata: str
    other_data: None
