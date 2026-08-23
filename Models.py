from pydantic import BaseModel, Field, PositiveInt, ConfigDict
from typing import Literal


class HubMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    zone: Literal["normal", "blocked", "restricted", "priority"] = "normal"
    color: str | None = None
    max_drones: PositiveInt | None = 1


class ConnectionMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    max_link_capacity: PositiveInt | None = 1


class HubModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(pattern=r"^[^- ]+$")
    x: int
    y: int
    metadata: HubMetadata | None


class ConnectionModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    huba: str
    hubb: str
    metadata: ConnectionMetadata | None
