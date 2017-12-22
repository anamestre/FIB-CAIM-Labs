from igraph import Graph
import sys
import numpy as np
from IPython import display
from igraph import plot
import matplotlib.pyplot as plt
import math

graphArray = []
nodeCount = 0
edgeCount = 0

def readGraph(graphPath):
	global graphArray
	global nodeCount
	global edgeCount

	graphDoc = open(graphPath, 'r')
	for line in graphDoc.readlines():
		temp = line.split(' ')
		graphArray.append((int(temp[0]),int(temp[1])))
		nodeCount = max(max(int(nodeCount), int(temp[0])),int(temp[1]))
		edgeCount += 1

def main(argv=None):

	#TASK 1

	clustering_coefficients = [] #Clustering coefficients
	avg_shortest_paths = [] #Avg shortest paths
	
	aux = [ i / 5 for i in range(20, -1, -1)]
	probabilities = [10 ** -i for i in aux]
	
	firstCC = 0
	firstASP = 0
	for i in range(0,21):
		watts = Graph.Watts_Strogatz(1, 1000, 4, probabilities[i])
		#Calcular global transitivity aka clustering coefficient
		clustering_coefficients.append(watts.transitivity_undirected()) 
		if(i == 0):
			firstCC = clustering_coefficients[0]
		clustering_coefficients[i] /= firstCC #normalizar
		
		#Calcular average shortest path
		avg_shortest_paths.append(watts.average_path_length(unconn=True))
		if(i == 0):
			firstASP = avg_shortest_paths[0]
		avg_shortest_paths[i] /= firstASP #normalizar

	print("Clustering Coefficients")
	print("--------------------------------------")
	print(clustering_coefficients)
	print("Avg Shortest Paths")
	print("--------------------------------------")
	print(avg_shortest_paths)
	print("")
	plt.plot(probabilities, clustering_coefficients, 's', probabilities, avg_shortest_paths, 'o')
	plt.xlabel('Probability')
	plt.xscale('log')
	plt.savefig('plot_task_1.png', bbox_inches='tight')
	plt.show()

	#TASK 2

	#Parte 1
	global graphArray
	readGraph('edges.txt')
	g = Graph()
	g.add_vertices(nodeCount+1)
	g.add_edges(graphArray)
	
	print("Edge count: " + repr(edgeCount))
	print("Node count: " + repr(nodeCount))
	print("Diameter: " + repr(g.diameter(directed=False)))
	print("Clustering Coeffiecient: " + repr(g.transitivity_undirected()))

	# Degree distribution 
	print("\nDegree distribution: ")
	print(g.degree_distribution())
	print(g.degree())

	# Plotear con tamaño de nodos en función de PageRank
	print("PageRank:")
	graphPageRank = g.pagerank()
	prPlot = plot(g, vertex_size = [graphPageRank[i]*500 for i in range(0,len(g.vs))])
	#Parte 2
	communityGraph = Graph.Erdos_Renyi(20,0.3)
	comGraphPlot = plot(communityGraph, layout = communityGraph.layout_kamada_kawai(),target="./comGraph.png")
	comGraphPlot.show()
	
	#Elegir algoritmo
	com = communityGraph.community_edge_betweenness()
	
	#Mostrar nodos comunidad más grande
	comCluster = com.as_clustering()
	comSizes = comCluster.sizes()
	print("Max community size: " + repr(max(comSizes)))
	
	#Plot histograma tamaños comunidad
	plt.hist(comSizes, bins=range(min(comSizes),max(comSizes) + 1, 1), align='left')
	plt.ylabel('Number of communities')
	plt.xlabel('Community size')
	plt.savefig('plot_hist_communities.png')
	plt.show()
	
	#Plot grafo comunidades
	communitiesPlot = plot(com.as_clustering(), layout = communityGraph.layout_kamada_kawai(),target="./com-comGraph.png")
	communitiesPlot.show()

if __name__ == "__main__":
    sys.exit(main())