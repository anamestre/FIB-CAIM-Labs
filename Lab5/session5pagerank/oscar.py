#!/usr/bin/python

from collections import namedtuple
from random import randint
import time
import sys

class Edge:
    def __init__ (self, origin=None):
        self.origin = origin
        self.weight = 1.

    def __repr__(self):
        return "edge: {0} {1}".format(self.origin, self.weight)

class Airport:
    def __init__ (self, iden=None, name=None):
        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict()
        self.outweight = 0.

    def addEdge (self, code):
        if code in self.routeHash:
            edge = self.routes[self.routeHash[code]]
            edge.weight += 1.
        else:
            edge = Edge(airportHash[code])
            self.routes.append(edge)
            self.routeHash[code] = len(self.routes)-1

    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.pageIndex)

airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> ID (AKA OpenFlights Identifier)
P = [] # list of weights

def readAirports(fd):
    print "Reading Airport file from {0}".format(fd)
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = len(airportList)-1
    airportsTxt.close()
    print "There were {0} Airports with IATA code".format(cont)


def readRoutes(fd):
    print "Reading Routes file from {0}".format(fd)
    routesTxt = open(fd, "r")
    cont = 0
    for line in routesTxt.readlines():
        try:
            temp = line.split(',')
            #print temp
            if len(temp[2]) != 3 :
                raise Exception('not an IATA code')
            if len(temp[4]) != 3 :
                raise Exception('not an IATA code')
                
            #Obtenir aeroport origen amb codi IATA
            o_code=temp[2]
            if o_code in airportHash:
                pass
            else:
                raise Exception('not airport found '+o_code)
            id_o=airportHash[o_code]
            o_airport = airportList[id_o]

            #Obtenir aeroport final amb codi IATA
            d_code=temp[4]
            if d_code in airportHash:
                pass
            else:
                raise Exception('not airport found '+d_code)
            id_d=airportHash[d_code]
            d_airport=airportList[id_d]

            #Afegim la ruta a la llista de aeroport final
            d_airport.addEdge(o_code)
            #Augmentar outweight (rutes sortints) de aeroport origen
            o_airport.outweight += 1.
        except Exception as inst:
            pass
        else:
            #Incrementem comptador
            cont += 1
    routesTxt.close()
    print "There were {0} Routes with IATA code".format(cont)

def checkStoppingCondition(A, B):
    th = 1e-15
    diff = map(lambda (a,b): abs(a-b), zip(A,B))
    return all(map(lambda x: x < th, diff))

def computePageRanks():
    global P
    n = len(airportList)
    P = [1./n]*n
    L = 0.85
    stopping_condition = False

    iterations = 0;
    while not stopping_condition:
        Q = [0.]*n
        for i in range(n):
            a = airportList[i]
            s = 0
            for r in a.routes:
                w = r.weight
                j = r.origin
                out = airportList[j].outweight
                s += P[j] * w / out
            Q[i] = L*s + (1-L)/n

        stopping_condition = checkStoppingCondition(P,Q)
        P = Q
        #assert abs(1.0 - sum(P)) < .0000000000001
        iterations += 1

    return iterations

def outputPageRanks():
    n = len(airportList)
    l = zip(range(n),P)
    l.sort(key=lambda x: x[1], reverse=True)
    for i,p in l:
        print p, airportList[i].name

def dealWithNullOutWeight(a):
    # we create an outgoing route to a random airport
    n = len(airportList)
    i = randint(0,n-1)
    d_airport = airportList[i]
    d_airport.addEdge(a.code)
    a.outweight += 1.

def checkNormalizedColumns():
    n = len(airportList)
    aux = [0]*n
    for a in airportList:
        for r in a.routes:
            w = r.weight
            j = r.origin
            out = airportList[j].outweight
            aux[j] += w/out
    for i,a in enumerate(airportList):
        assert abs(1.0 - aux[i]) < .0000000000001

def initExample():
    # toy example from the course slides
    airports = []
    A = Airport('AAA','AAA'); airports.append(A)
    B = Airport('BBB','BBB'); airports.append(B)
    C = Airport('CCC','CCC'); airports.append(C)
    D = Airport('DDD','DDD'); airports.append(D)
    for a in airports:
        airportList.append(a)
        airportHash[a.code] = len(airportList)-1

    A.addEdge('AAA')
    A.addEdge('BBB')
    B.addEdge('CCC')
    B.addEdge('DDD')
    C.addEdge('AAA')
    D.addEdge('AAA')
    D.addEdge('BBB')
    D.addEdge('CCC')

    A.outweight = 3.
    B.outweight = 2.
    C.outweight = 2.
    D.outweight = 1.


def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    #initExample()

    for a in airportList: 
        if a.outweight == 0: dealWithNullOutWeight(a)
    
    checkNormalizedColumns()

    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()

    outputPageRanks()
    print "Sum of weights:", sum(P)
    print "#Iterations:", iterations
    print "Time of computePageRanks():", time2-time1


if __name__ == "__main__":
    sys.exit(main())