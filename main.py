from Visualiser import Visualiser
from ProcessMap import ProcessMap
from Graph import Graph

if __name__ == "__main__":
    proccess = ProcessMap("C:\\Users\\kulag\\Desktop\\flyin\\Fly-in\\maps\\test\\two_ways.txt")
    graph = Graph(
        proccess.connections, proccess.start_hub,
        proccess.end_hub, proccess.hubs, proccess.drones)
    graph.path_finder()
    graph.path_finder()
    #graph.print_output_more()
    #visualiser = Visualiser(proccess)
    #visualiser.run()