#!/usr/bin/python

from collections import namedtuple
import time
import sys

# TODO: acabar classe
class Route:
    def __init__ (self, code = None, opCode = None, origin = None,
                  originOp = None, destination = None, destinationOp = None):
        self.code = code
        self.opCode = opCode
        self.origin = origin
        self.originOp = originOp
        self.destination = destination
        self.destinationOp = destinationOp
        #self. otherStuff = otherStuff

# Edge: each edge has the origin code of an airport and its weight.
class Edge:
    def __init__ (self, origin = None, index = None):
        self.origin = origin
        self.weight = 1					# how many times there's a route from origin to an specific airport
        self.index = index 				# Index dins de airportList

    def __repr__(self):
        return "edge: {0} {1}".format(self.origin, self.weight)
        
    ## write rest of code that you need for this class

class Airport:
    def __init__ (self, iden=None, name=None, index = None):
        self.code = iden				# IATA code
        self.name = name 				# Name of the airport
        self.routes = []				# list of edges of the airports that have this airport as destination; list[edges]
        self.routeHash = dict()			# dict{key = airport IATA code : index in routes}
        self.outweight = 0				# weight from this airport to others
        self.index = index

    def addEdge(self, origCode):
        if origCode in self.routeHash:
            index = self.routeHash[origCode]
            edge = self.routes[index]
            edge.weight += 1
        else:
            pos = airportHash[origCode].index # aixo retorna un aeroport
            #print "adding edge index = " + pos
            edge = Edge(origCode, pos)

            self.routes.append(edge)
            index = len(self.routes) - 1
            self.routeHash[origCode] = index

    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.pageIndex)
        	


edgeList = [] # list of Edges
edgeHash = dict() # hash of edge to ease the match
airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport
routeList = []
routeHash = dict()
pageR = []

def readAirports(fd):
    print "Reading Airport file from {0}".format(fd)
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :  # Is this OK????! != 5?!?!?!
                raise Exception('not an IATA code')
            a.name = temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code = temp[4][1:-1]
            a.index = cont
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()
    print "There were {0} Airports with IATA code".format(cont)

def getAirport(code):
	print ":)"
	try:
		if not(code in airportHash):
			raise Exception ("Airport " + code + " not found.")
			print "no code" + str(code)
		else:
			print code
			index = airportHash[code].index
			print index
			return airportList[index]
	except Exception as inst:
		pass


# TODO: comprovar que funciona
def readRoutes(fd):
    # airline code, op airline code, origin airport code, op origin code, 
    # dest airport code, op destination airport code
    # nomes mirarem els que tenen IATA codes -> aka 3 lletres al codi de l'aeroport. (no op)
    print "Reading Routes file from {0}".format(fd)
    
    routesTxt = open(fd, "r");
    cont = 0
    for line in routesTxt.readlines():
        try: 
            temp = line.split(',')
            if len(temp[2]) != 3 or len(temp[4]) != 3:
                raise Exception('not an IATA code')
            
            codeO = temp[2]
            codeD = temp[4]
            
            if not(codeO in airportHash):
              raise Exception ("Airport not found.")
            
            index = airportHash[codeO].index
            oAirp = airportList[index]
            
            if not(codeD in airportHash):
                raise Exception ("Airport not found.")
            
            index = airportHash[codeD].index
            dAirp = airportList[index]
            
            dAirp.addEdge(codeO)
            oAirp.outweight += 1
        except Exception as inst:
            pass
        else:
            cont += 1
            
    routesTxt.close()
    print "There were {0} Airports with IATA code".format(cont)

def checkStoppingCondition(A, B):
    th = 1e-15
    diff = map(lambda (a,b): abs(a-b), zip(A,B))
    return all(map(lambda x: x < th, diff))

# TODO: adaptar pageRank al meu codi
def computePageRanks():
        print "Computing Page Rank"
        n = len(airportList)
        n2 = 1./n
        P = [n2]*n
        L = 0.85
        iters = 0
        stop = False
        pageR = P
        while not stop:
            Q = [0]*n
            for i in range(n):
                    airp = airportList[i]
                    suma = 0
                    # edge = route
                    for edge in airp.routes:
                        w = edge.weight
                        out = airportList[edge.index].outweight
                        suma += P[edge.index] * w / out 
                        L1 = (1 - L)/n
                        Q[i] = L * suma + L1
            #print "and while again :)"
        P = Q
        stop = checkStoppingCondition(P, Q)
        iters += 0
    
        pageR = P
        return iters
     

# Print list of airports
def outputPageRanks():
    n = len(airportList)
    myList = dict([(key, a) for key in range(n) for a in pageR])
    myNewList = sorted(myList.items, key = operator.itemgetter(1), reverse = True) # sort by value, >=
    index = 1
    print "Airports ordered by PageRank:"
    for airp in myNewList:
        name = airportList[airp].name
        code = airportList[airp].code
        print  index + '. ' + name + ' [' + code + '], PageRank = ' + myNewList[airp]
        index += 1



def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")

   # for x in range(20):
    #    print airportList[x].routes

    #for x in airportHash:
       # print airportHash[x].routes

    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    print "#Iterations:", iterations
    #print "Time of computePageRanks():", time2-time1


if __name__ == "__main__":
    sys.exit(main())
