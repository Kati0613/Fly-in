

class MapReader:
    def __init__(self, map_file):
        self.map_file = map_file
        self.start_hub = ""
        self.end_hub = ""
        self.hubs = []
        self.connections = []
        self.nb_of_drones = ""
        self.validate_map()

    def validate_map(self):
        start = True
        try:
            with open(self.map_file, 'r') as file:
                for line in file:
                    if line[0] == "#":
                        continue
                    elif start:
                        if "nb_drones" in line:
                            self.nb_of_drones = line
                            start = False
                            continue
                        else:
                            raise ValueError(
                                "Map should start with a number "
                                "of drones. Please provide a valid map")
                    elif line.strip() == "":
                        continue
                    status = self.validate_line(line)
                    if status == 0:
                        continue
                    elif status == 1:
                        raise ValueError("Map should have only one start hub")
                    elif status == 2:
                        raise ValueError("Map should have only one end hub")
                    elif line.split()[0] == "hub:":
                        self.hubs.append(line.split())
                    elif line.split()[0] == "connection:":
                        self.connections.append(line.split())
                    else:
                        raise ValueError(
                            f"""{line.split()[0]} is not a valid parameter.
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

    def validate_line(self, line):
        if "start_hub:" in line and self.start_hub == "":
            self.start_hub = line
            return 0
        elif "start_hub:" in line and self.start_hub != "":
            return 1
        elif "end_hub:" in line and self.end_hub == "":
            self.end_hub = line
            return 0
        elif "end_hub:" in line and self.start_hub != "":
            return 2
