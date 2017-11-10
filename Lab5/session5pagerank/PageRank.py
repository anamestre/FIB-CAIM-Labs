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

# TODO: acabar classe
class Edge:
    def __init__ (self, origin=None):
        self.origin = origin
        self.weight = 1

    def __repr__(self):
        return "edge: {0} {1}".format(self.origin, self.weight)
        
    ## write rest of code that you need for this class

# TODO: acabar classe
class Airport:
    def __init__ (self, iden=None, name=None):
        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict()
        self.outweight = 0

    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.pageIndex)
    
    # TODO
    def addEdge(self, edge):
        self.outweight += 1

edgeList = [] # list of Edge
edgeHash = dict() # hash of edge to ease the match
airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport
routeList = []
routeHash = dict()

def readAirports(fd):
    print "Reading Airport file from {0}".format(fd)
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 3 :
                raise Exception('not an IATA code')
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()
    print "There were {0} Airports with IATA code".format(cont)


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
            r = Route(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5]) # de moment no guardarem "otherStuff"
        except Exception as inst:
            pass
        else:
            cont += 1
            routeList.append(r)
            routeList[r.code] = r
    routesText.close()
    print "There were {0} Airports with IATA code".format(cont)


# TODO: adaptar pageRank al meu codi
def computePageRanks():
    n = len(airportList)
    n2 = 1/n
    P = [n2]*n
    L = 0.85
    while (not stop) {
        Q = [0]*n
        for i in range(0, n - 1):
            # TODO: w, out
            Q[i] = L * sum(P[j]*w(j,i)/out(j) for j in range(0, n-1) '''if hi ha edge''') + (1-L)/n;
        P = Q
    }
    

# TODO: implementar
def outputPageRanks():
    # write your code

def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    #time1 = time.time()
    #iterations = computePageRanks()
    #time2 = time.time()
    #outputPageRanks()
    print "#Iterations:", iterations
    print "Time of computePageRanks():", time2-time1


if __name__ == "__main__":
    sys.exit(main())
