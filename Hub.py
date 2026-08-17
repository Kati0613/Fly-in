from typing import List
from Models import HubModel


class Hub:
    def __init__(self, x: str, y: str, metadata: str, other_data: List | None =None):
        validated_data = HubModel(
            x=x, y=y, metadata=metadata, other_data=other_data
            )

        self.x = validated_data.x
        self.y = validated_data.y
        self.metadata = validated_data.metadata