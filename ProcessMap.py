from Hub import Hub
from Connection import Connection


class ProcessMap:
    def __init__(self, map_file):
        self.map_file = map_file
        self.start_hub = ""
        self.end_hub = ""
        self.hubs = dict()
        self.connections = []
        self.nb_of_drones = ""
        self.unique_connections = list()
        self.unique_coords = list()
        self.min_h = ""
        self.min_w = ""
        self.max_h = ""
        self.max_w = ""
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
                        self.validate_coords(splitted_line[2:4])
                        metadata = self.procces_metadata(splitted_line[4:])
                        self.start_hub = Hub(splitted_line[1],
                                             splitted_line[2],
                                             splitted_line[3], metadata,
                                             False, True)
                        self.hubs[splitted_line[1]] = self.start_hub
                    elif "end_hub:" == splitted_line[0]:
                        self.validate_start_end(splitted_line[0],
                                                splitted_line[1])
                        self.validate_coords(splitted_line[2:4])
                        metadata = self.procces_metadata(splitted_line[4:])
                        self.end_hub = Hub(splitted_line[1], splitted_line[2],
                                           splitted_line[3], metadata,
                                           False, True)
                        self.hubs[splitted_line[1]] = self.end_hub
                    elif splitted_line[0] == "hub:":
                        self.validate_names(splitted_line[1])
                        self.validate_coords(splitted_line[2:4])
                        metadata = self.procces_metadata(splitted_line[4:])
                        hub = Hub(splitted_line[1], splitted_line[2],
                                  splitted_line[3], metadata)
                        self.hubs[splitted_line[1]] = hub
                    elif splitted_line[0] == "connection:":
                        huba, hubb = self.validate_connection(splitted_line[1])
                        metadata = self.procces_metadata(splitted_line[2:])
                        self.connections.append(Connection(
                            self.hubs[huba], self.hubs[hubb], metadata
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
            or len(self.connections) < (len(self.hubs)  - 1)
            or len(self.connections) > ((len(self.hubs))
                                        * (len(self.hubs) - 1))/2):
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
        if self.hubs.get(name):
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

        if not (self.hubs.get(huba) and self.hubs.get(hubb)):
            raise ValueError(
                "Invalid connection. Use a proper hub names or add a new ones."
            )
        else:
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
            return huba, hubb

    def validate_coords(self, xy: list):
        if (xy in self.unique_coords):
            raise ValueError("Coords should be unique.")
        else:
            xy[0] = int(xy[0])
            xy[1] = int(xy[1])
            if self.max_w == "":
                self.max_w = xy[0]
                self.max_h = xy[1]
                self.min_w = xy[0]
                self.min_h = xy[1]
            else:
                if self.max_w < xy[0]:
                    self.max_w = xy[0]
                elif self.min_w > xy[0]:
                    self.min_w = xy[0]

                if self.max_h < xy[1]:
                    self.max_h = xy[1]
                elif self.min_h > xy[1]:
                    self.min_h = xy[1]

        self.unique_coords.append(xy)

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

    def get_width_height(self):
        return ((self.max_w - self.min_w + 1), (self.max_h - self.min_h + 1))
