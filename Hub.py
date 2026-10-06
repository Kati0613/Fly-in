from Models import HubModel


class Hub:
    def __init__(self, name: str, x: str, y: str, metadata: dict | None = None,
                 start: bool = False, end: bool = False, drones: int = 0):
       

        validated_data = HubModel(
            name=name, x=x, y=y, metadata=metadata,
            )

        self.name = validated_data.name
        self.x = validated_data.x
        self.y = validated_data.y
        if start or end:
            self.metadata.max_drones = None
        else:
            self.metadata = validated_data.metadata
        self.start = start
        self.end = end
        self.drones = drones
