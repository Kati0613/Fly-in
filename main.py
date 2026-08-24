from Visualiser import Visualiser
from ProcessMap import ProcessMap
from Graph import Graph

if __name__ == "__main__":
    proccess = ProcessMap("/nfs/homes/kkulagow/fly-in/maps/easy/01_linear_path.txt")
    graph = Graph(proccess.connections)
