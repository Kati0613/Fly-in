

class Graph():

    def __init__(self, connections):
        self.neighbours = dict()

        for connection in connections:
            if not self.neighbours.get(connection.huba):
                self.neighbours[connection.huba] = [connection]
            else:
                self.neighbours[connection.huba].append(connection)
            if not self.neighbours.get(connection.hubb):
                self.neighbours[connection.hubb] = [connection]
            else:
                self.neighbours[connection.huba].append(connection)

        print(self.neighbours)
            


