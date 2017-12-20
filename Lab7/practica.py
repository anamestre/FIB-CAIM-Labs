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

	clustering_coefficients = [] #Aqui iran los clustering coefficients
	avg_shortest_paths = [] #Aqui iran los avg shortest paths
	increment = 1./14.
	probabilities = [i*increment for i in range(0,14)] #Probabilidades, jugar con ellas
	for i in range(0,14):
		watts = Graph.Watts_Strogatz(1,100,2,probabilities[i])
		clustering_coefficients.append(watts.transitivity_undirected()) #Calcular global transitivity aka clustering coefficient
		clustering_coefficients[i] /= clustering_coefficients[0] #ir dividiendo entre el primero para normalizar
		#no se como hacer bien esto. Cuando un nodo no esta conectado, su shortest path es inf
		#por tanto, toda la media ya da inf. Hay que quitar los inf pero no sé si ponerlos a 0, o 
		#eliminarlos, de momento los he eliminado, a la espera de correo del bejar

		counter = 0
		sumPath = 0
		sp1 = watts.shortest_paths(mode='ALL')
		for arr in sp1:
			for val in arr:
				if not math.isinf(val):
					counter += 1
					sumPath += val
		avg_shortest_paths.append(sumPath/float(counter))
		avg_shortest_paths[i] /= avg_shortest_paths[0] #normalizar

	print(clustering_coefficients)
	print(avg_shortest_paths)

	#Aqui hay que hacer el plot pero jamás he conseguido que quede como el del enunciado
	#no entiendo bien la escala logaritmica de X. TODO
	plt.plot(probabilities, clustering_coefficients, 's')
	plt.show()

	#TASK 2

	#Part 1
	#Leer grafo
	global graphArray
	readGraph('edges.txt')
	g = Graph()
	g.add_vertices(nodeCount+1)
	g.add_edges(graphArray)

	#edges
	print(edgeCount)
	#nodes
	print(nodeCount)
	#diameter
	print(g.diameter(directed=False))
	#transitivity
	print(g.transitivity_undirected())
	#degree distribution TODO: Hacer plot
	print(g.degree_distribution())

	#Parte 2 (Copiar del jupyter de bejar)

	#Elegir algoritmo
	#Ejecutar
	#Mostrar nodos comunidad más grande
	#Plot histograma tamaños comunidad
	#Plot grafo comunidades
if __name__ == "__main__":
    sys.exit(main())