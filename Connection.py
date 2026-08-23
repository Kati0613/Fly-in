from Models import ConnectionModel


class Connection:

    def __init__(self, huba: str, hubb: str, metadata: dict | None = None):
        validated_data = ConnectionModel(huba=huba, hubb=hubb,
                                         metadata=metadata)

        self.huba = validated_data.huba
        self.hubb = validated_data.hubb
        self.metadata = validated_data.metadata
