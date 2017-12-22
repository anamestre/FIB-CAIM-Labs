from igraph import Graph
import sys
import numpy as np
from IPython import display
from igraph import plot
import matplotlib.pyplot as plt
import math

'''TODO:
	- Dejar los plots bien, se me dan un poco mal, tu sabrás dejarlos bonitos.
	- Comentar y analizar cosas
	- Algún TODO que falta por ahí en medio
	- A pesar del correo del Béjar sigo sin estar seguro que si es transitivity_undirected
	o transitivity_local_undirected, creo que es la primera pero not sure, a ver
	que opinas tu
	- La docu'''

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

	clustering_coefficients = [] #Aqui irán los clustering coefficients
	avg_shortest_paths = [] #Aqui irán los avg shortest paths
	increment = 1./14.
	probabilities = [i*increment for i in range(0,14)] #Probabilidades, jugar con ellas
	firstCC = 0
	firstASP = 0
	for i in range(0,14):
		watts = Graph.Watts_Strogatz(1,100,2,probabilities[i])
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
	plt.xscale('log')
	plt.savefig('plot_task_1.png', bbox_inches='tight')
	plt.show()

	#TASK 2

	#Parte 1

	#Leer grafo
	global graphArray
	readGraph('edges.txt')
	g = Graph()
	g.add_vertices(nodeCount+1)
	g.add_edges(graphArray)

	#edges
	print("Edge count: " + repr(edgeCount))
	#nodes
	print("Node count: " + repr(nodeCount))
	#diameter
	print("Diameter: " + repr(g.diameter(directed=False)))
	#transitivity
	print("Clustering Coeffiecient: " + repr(g.transitivity_undirected()))

	#degree distribution TODO: Con el print ya la sabemos y no nos pide plot,
	#pero igual es más fácil de ver, lo dejo a tu criterio
	print("\nDegree distribution: ")
	print(g.degree_distribution())

	#Plotear con tamaño de nodos en función de PageRank
	graphPageRank = g.pagerank()
	prPlot = plot(g, vertex_size = [graphPageRank[i]*500 for i in range(0,len(g.vs))])
	
	#Parte 2

	#Crear grafo, cambia el generador si prefieres otro
	communityGraph = Graph.Erdos_Renyi(20,0.3)
	comGraphPlot = plot(communityGraph, layout = communityGraph.layout_kamada_kawai(),target="./comGraph.png")
	comGraphPlot.show()
	#Elegir algoritmo (si te gusta otro cambialo)
	com = communityGraph.community_edge_betweenness()
	#Mostrar nodos comunidad más grande
	comCluster = com.as_clustering()
	comSizes = comCluster.sizes()
	print("Max community size: " + repr(max(comSizes)))
	#Plot histograma tamaños comunidad
	plt.hist(comSizes, bins=max(comSizes))
	plt.savefig('plot_hist_communities.png', bbox_inches='tight')
	plt.show()
	#Plot grafo comunidades
	communitiesPlot = plot(com.as_clustering(), layout = communityGraph.layout_kamada_kawai(),target="./com-comGraph.png")
	communitiesPlot.show()
	
if __name__ == "__main__":
    sys.exit(main())