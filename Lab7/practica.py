from igraph import Graph
import sys
import numpy as np
from IPython import display
from igraph import plot
import math

graphArray = []
nodeCount = 0

def readGraph(graphPath):
	global graphArray
	global nodeCount

	graphDoc = open(graphPath, 'r')
	for line in graphDoc.readlines():
		temp = line.split(' ')
		graphArray.append((int(temp[0]),int(temp[1])))
		nodeCount = max(max(int(nodeCount), int(temp[0])),int(temp[1]))

def main(argv=None):
	'''global graphArray
	readGraph('caimlab1617.txt')
	g = Graph()
	g.add_vertices(nodeCount+1)
	g.add_edges(graphArray)
	print(g)'''

	clustering_coefficients = []
	avg_shortest_paths = []
	increment = 1./14.
	for i in range(0,14):
		watts = Graph.Watts_Strogatz(1,100,2,i*increment)
		clustering_coefficients.append(watts.transitivity_undirected())
		sp1 = watts.shortest_paths(mode='ALL')
		sp1 = sp1[np.isfinite(sp1)]
		avg_shortest_paths.append(np.mean(sp1))
	print(clustering_coefficients)
	print(avg_shortest_paths)
if __name__ == "__main__":
    sys.exit(main())