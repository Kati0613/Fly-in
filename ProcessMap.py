from Hub import Hub
from Connection import Connection

class ProcessMap:
    def __init__(self, map_file):
        self.map_file = map_file
        self.start_hub = ""
        self.end_hub = ""
        self.hubs = []
        self.connections = []
        self.nb_of_drones = ""
        self.unique_names = dict()
        self.unique_connections = list()
        self.validate_map()

    def validate_map(self):
        start = True
        try:
            with open(self.map_file, 'r') as file:
                for line in file:
                    splitted_line = line.split()

                    if line[0] == "#":
                        continue
                    elif start:
                        if "nb_drones" in splitted_line[0]:
                            try:
                                self.nb_of_drones = int(splitted_line[1])
                                start = False
                                if self.nb_of_drones <= 0:
                                    raise ValueError(
                                        "Number of drones must be positive"
                                    )
                                continue
                            except ValueError:
                                raise ValueError(
                                    "Please use a correct number"
                                )
                        else:
                            raise ValueError(
                                "Map should start with a number "
                                "of drones. Please provide a valid map")
                    elif line.strip() == "":
                        continue

                    if "start_hub:" == splitted_line[0]:
                        self.validate_start_end(splitted_line[0],
                                                splitted_line[1])
                        metadata = self.procces_metadata(splitted_line[4:])
                        self.start_hub = Hub(splitted_line[1],
                                             splitted_line[2],
                                             splitted_line[3], metadata,
                                             False, True)
                    elif "end_hub:" == splitted_line[0]:
                        self.validate_start_end(splitted_line[0],
                                                splitted_line[1])
                        metadata = self.procces_metadata(splitted_line[4:])
                        self.end_hub = Hub(splitted_line[1], splitted_line[2],
                                           splitted_line[3], metadata,
                                           False, True)
                    elif splitted_line[0] == "hub:":
                        self.validate_names(splitted_line[1])
                        metadata = self.procces_metadata(splitted_line[4:])
                        self.hubs.append(Hub(splitted_line[1],
                                             splitted_line[2],
                                             splitted_line[3], metadata))
                    elif splitted_line[0] == "connection:":
                        self.validate_connection(splitted_line[1])
                        metadata = self.procces_metadata(splitted_line[2:])
                        self.connections.append(Connection(
                            splitted_line[1], metadata
                        ))
                    else:
                        raise ValueError(
                            f"""{splitted_line[0]} is not a valid parameter.
                            Please provide a valid map file"""
                            )

        except FileNotFoundError:
            raise FileNotFoundError(
                "Map file not found. Please provide a valid map file.")

        if (self.start_hub == "" or self.end_hub == ""
            or len(self.connections) < (len(self.hubs) + 1)
            or len(self.connections) > ((len(self.hubs) + 2)
                                        * (len(self.hubs) + 1))/2):
            raise ValueError(
                "You must provide atleast one start_hub, "
                "end_hub and enough connections"
                )

    def validate_start_end(self, obj_name, name):
        if "start_hub:" in obj_name and self.start_hub == "":
            self.validate_names(name)
        elif "start_hub:" in obj_name and self.start_hub != "":
            raise ValueError("Map should have only one start hub")
        elif "end_hub:" in obj_name and self.end_hub == "":
            self.validate_names(name)
        elif "end_hub:" in obj_name and self.start_hub != "":
            raise ValueError("Map should have only one end hub")

    def validate_names(self, name):
        if not self.unique_names.get(name):
            self.unique_names[name] = 1
        else:
            raise ValueError("Your name must be unique")
        if "-" in name or " " in name:
            raise ValueError(
                f"Invalid character in name {name}."
                "Please do not use '-' or ' '"
                "."
                )

    def validate_connection(self, connection):
        huba = connection[0:connection.find("-")]
        hubb = connection[connection.find("-")+1:]

        if not self.unique_names.get(huba) and not self.unique_names.get(hubb):
            raise ValueError(
                "Invalid connection. Use a proper hub names or add a new ones."
            )
        elif self.unique_names.get(huba) and self.unique_names.get(hubb):
            if connection in self.unique_connections:
                raise ValueError(
                    "Invalid connection. There should be no dupplicate."
                )
            reversed_connection = hubb + "-" + huba
            if reversed_connection in self.unique_connections:
                raise ValueError(
                    "Invalid connection. There should be no dupplicate."
                )
            self.unique_connections.append(connection)

    def procces_metadata(self, metadata):
        metadata = " ".join(metadata)
        if metadata is None or metadata == "":
            return None

        pairs = []
        if (metadata[0] != "[" or metadata[-1] != "]"):
            raise ValueError("Provide a proper metadata. It should be in []")
        else:
            metadata = metadata[1:-1].split()
            for data in metadata:
                pair = data.split("=", 1)
                pairs.append(pair)

        try:
            proccesed_metadata = dict(pairs)
        except ValueError:
            raise ValueError(
                "Incorrect metadata. "
                "Remember - all data must have key and value separeted by ="
            )
        return proccesed_metadata






