from Models import ConnectionModel


class Connection:

    def __init__(self, connection:str, metadata:str, other_data=None):
        validated_data = ConnectionModel(connection=connection, metadata=metadata, other_data=other_data)

        self.connection = validated_data.connection
        self.metadata = validated_data.metadata
        

