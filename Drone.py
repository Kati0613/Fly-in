class Drone:
    def __init__(self, name, start_hub):
        self.name = name
        self.current_hub = start_hub
        self.step = 1