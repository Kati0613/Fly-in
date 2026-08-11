

class MapReader:
    def __init__(self, map_file):
        self.map_file = map_file
        self.start_hub = ""
        self.end_hub = ""
        self.hubs = []
        self.connections = []

    def get_valid_map_data(self):
        start = True
        try:
            with open(self.map_file, 'r') as file:
                for line in file:
                    if line[0] == "#":
                        continue
                    elif start:
                        if "nb_drones" in line:
                            self.data.append(line)
                            start = False
                            continue
                        else:
                            raise ValueError("Map should start with a number of drones. Please provide a valid map")
                    elif line.strip() == "":
                        continue
                    status = self.validate_line(line)[0]
                    if status == 1:
                        raise ValueError("Map should have only one start hub")
                    elif status == 2:
                        raise ValueError("Map should have only one end hub")
                    elif line.split()[0] == "hub:":
                        self.hubs.append(line.split())
                    elif line.split()[1] == "connections:":
                        self.connections.append(line.split())
                    else:
                        raise ValueError(f"{line.split()[0]} is not a valid parameter. Please provide a valid map file")
        except FileNotFoundError:
            raise FileNotFoundError("Map file not found. Please provide a valid map file.")

        if self.start_hub ==  "" or self.end_hub == "" or len(self.connections) - 1 < len(self.hubs) + 2:
            raise ValueError("You must provide atleast one start_hub, end_hub and enough connections")
        
        return self.data

    def validate_line(self, line):
        if "start_hub" in line and self.start_hub == "":
            return 0
        elif "start_hub" in line and self.start_hub !="":
            return 1
        elif "end_hub" in line and self.end_hub == "":
            return 0
        elif "start_hub" in line and self.start_hub !="":
            return 2

