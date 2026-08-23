from Models import ConnectionModel


class Connection:

    def __init__(self, connection: str, metadata: dict | None = None):
        validated_data = ConnectionModel(connection=connection,
                                         metadata=metadata)

        self.connection = validated_data.connection
        self.metadata = validated_data.metadata
