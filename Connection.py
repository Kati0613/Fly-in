from Models import ConnectionModel
from Hub import Hub


class Connection:

    def __init__(self, huba: Hub, hubb: Hub, metadata: dict | None = None):
        validated_data = ConnectionModel(metadata=metadata)

        self.huba = huba
        self.hubb = hubb
        self.metadata = validated_data.metadata
