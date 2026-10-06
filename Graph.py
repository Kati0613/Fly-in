

from Connection import Connection


class Graph():

    def __init__(self, connections, start, end, hubs, drones):
        self.neighbours = dict()
        self.start = start
        self.end = end
        self.hubs = hubs
        self.drones = drones
        self.connections = connections
        self.paths = []

        for connection in connections.values():
            if not self.neighbours.get(connection.huba):
                self.neighbours[connection.huba] = [connection]
            else:
                self.neighbours[connection.huba].append(connection)
            if not self.neighbours.get(connection.hubb):
                self.neighbours[connection.hubb] = [connection]
            else:
                self.neighbours[connection.huba].append(connection)


    def find_shortes_path(self):
        self.parents = dict()
        unvisited = [self.start]
        visited = []
        self.parents[self.start] = None
        path = []
        while True:
            current = unvisited.pop(0)
            for connection in self.neighbours[current]:
                if connection.huba.name != current.name and connection.huba not in visited and connection.huba not in unvisited:
                    unvisited.append(connection.huba)
                    self.parents[connection.huba] = current
                elif connection.hubb.name != current.name and connection.hubb not in visited and connection.hubb not in unvisited:
                    unvisited.append(connection.hubb)
                    self.parents[connection.hubb] = current
            visited.append(current)
            if current == self.end:
                break
        node = self.end
        while node is not None:
            path.append(node.name)
            node = self.parents[node]
        path.reverse()
        #print(path)
           
    #weighted path finder
    def path_finder(self):
        weight_path = {i:[float('inf'), None] for i in self.hubs.values()}
        unvisited = self.hubs.copy()
        visited = []
        current = self.start
        weight_path[self.start][0] = 0 
        zone_cost = {"normal": 1, "blocked": float("inf"), "restricted": 2, "priority": 1}
        self.path = []
        while current != self.end:
            for link in self.neighbours[current]:
                if link.huba != current:
                    weight = zone_cost[link.huba.metadata.zone]
                    distance = weight_path[current][0] + weight

                    if distance < weight_path[link.huba][0]:
                        weight_path[link.huba][0] = distance
                        weight_path[link.huba][1] = current

                if link.hubb != current:
                    weight = zone_cost[link.hubb.metadata.zone]
                    distance = weight_path[current][0] + weight

                    if distance < weight_path[link.hubb][0]:
                        weight_path[link.hubb][0] = distance
                        weight_path[link.hubb][1] = current

            visited.append(current)
            unvisited.pop(current.name)
            current = self.get_min_distance_node(weight_path, visited)

        node = self.end
        restr = False
        while node is not None:
            if node.metadata.zone == "restricted" and restr == False:
                restr = True
            elif restr == True: 
                connection = self.path[-1].name + "-" + node.name
                if self.connections.get(connection) is not None:
                    self.path.append(self.connections[connection])
                else:
                    connection = node.name + "-" + self.path[-1].name
                    self.path.append(self.connections[connection])

                if node.metadata.zone != "restricted":
                    restr = False
            self.path.append(node) #pomysł: można by odrazu dodawać ścieżke jakby była ona częścią drogi - być może to coś  skróci
            node = weight_path[node][1]

        self.path.reverse()
        self.hubs[self.path[-1]].metadata.zone = "blocked"
        self.paths.append(self.path)
        print(self.path)
        

    def get_min_distance_node(self, weight_path, visited):
        min = float('inf')
        min_node = self.start
        for node, distance_prev in weight_path.items():
            if node not in visited:
                if distance_prev[0] < min:
                    min = distance_prev[0]
                    min_node = node 
                elif distance_prev[0] == min:
                    if node.metadata.zone == "priority":
                        min_node = node
        return min_node

    def print_output_more(self):
        while self.end.drones < len(self.drones):
            for drone in self.drones.values():
                i = drone.step
                if (i < len(self.path) and type(self.path[i]) == Connection and 
                (self.path[i].metadata is None or self.path[i].drones < self.path[i].metadata.max_link_capacity)):
                    drone.current_hub.drones -= 1
                    drone.current_hub = self.path[i]
                    print(f" {drone.name}-{self.path[i].huba.name}-{self.path[i].hubb.name}", end = "")
                    self.path[i].drones += 1
                    drone.step += 1  
                elif i < len(self.path) and (self.path[i].metadata.max_drones is None or self.path[i].drones < self.path[i].metadata.max_drones):
                    drone.current_hub.drones -= 1
                    drone.current_hub = self.path[i]
                    self.path[i].drones += 1
                    print(f" {drone.name}-{drone.current_hub.name}", end = "")
                    drone.step += 1    
            print()
            

    def print_output(self, drone = "D1"):
        prev = self.start
        for hub in self.path[1:]:
            if hub.metadata.zone == "restricted":
                print(f"{drone}-{prev.name}-{hub.name}")
                print(f"{drone}-{hub.name}")
            else:
                print(f"{drone}-{hub.name}")

            prev = hub

