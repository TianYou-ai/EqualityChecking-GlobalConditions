# -*- coding: utf-8 -*-
import random
import copy

from tools import plot_graph, show_details, is_connected

def get_nodes_num(num, israndom = False):
    if israndom == False:
        return num
    else:
        return random.randint(2, num)

def get_degree_num(num, israndom = False):
    if israndom == False:
        return num
    else:
        return random.randint(0, num)

class Vertex:
    def __init__(self,key):
        self.id = key
        self.connectedTo = {}
        self.name = None
        self.ifPointer = False
        self.childBlock = None
        self.condition = None
        self.value = key

    def addNeighbor(self,nbr,weight = 1):
        self.connectedTo[nbr] = weight

    def removeNeighbor(self, nbr):
        if nbr in self.connectedTo.keys():
            del self.connectedTo[nbr]

    def __str__(self):
        return str(self.id) + 'connectedTo' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return  self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self,nbr):
        return  self.connectedTo[nbr]

    def addBlock(self, block):
        self.ifPointer = True
        self.childBlock = block

    def isPointer(self):
        return self.ifPointer

    def setCondition(self, label):
        self.condition = label

class Graph:
    def __init__(self, Graph_name = None):
        self.vertList = {}
        self.numVertices = 0
        self.Graph_name = Graph_name

    def __len__(self):
        return len(self.getVertices())

    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        newVertex.name = "{}-{}".format(self.Graph_name, key)
        self.vertList[key] = newVertex
        return  newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return  self.vertList[n]
        else:
            return  None

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self,f,t,const = 1):
        if f not in self.vertList:
            self.addVertex(f)
        if t not  in self.vertList:
            self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t],const)

    def removeEdge(self, f, t):
        if f in self.vertList and t in self.vertList:
            self.vertList[f].removeNeighbor(self.vertList[t])

    def getEdgesKey(self):
        Edges = list()
        for v in self.vertList.values():
            for w in v.getConnections():
                Edges.append((v.id, w.id))
        return Edges

    def getEdges(self):
        Edges = list()
        for v in self.vertList.values():
            for w in v.getConnections():
                Edges.append((v.name, w.name))
        return Edges

    def getVertices(self):
        return  self.vertList.keys()

    def getVerticesNames(self):
        return [v.name for v in self.vertList.values()]

    def __iter__(self):
        return  iter(self.vertList.values())

    def getOutdegree(self, v):
        return len(self.vertList[v].getConnections())

    def getIndegree(self, v):
        indegree = 0
        for vert in self.vertList.values():
            for w in vert.getConnections():
                if w.getId() == v:
                    indegree += 1
        return indegree

    def addPointer(self, key, block):
        self.getVertex(key).addBlock(block)

    def setCondition(self, key, label):
        self.getVertex(key).setCondition(label)

    def getCondition(self, key):
        return self.getVertex(key).condition

    def clone(self):
        return copy.copy(self)

def create_graph(nodes_num, indegree_num, outdegree_num, name, if_connected = True):
    nodes_num = get_nodes_num(nodes_num)
    g = Graph(name)
    max_indegree_num = indegree_num
    for i in range(nodes_num):
        g.addVertex(i)
    for f in range(len(g.getVertices())):
        f_outdegree_num = get_degree_num(outdegree_num, israndom = True)
        nbrList = random.sample(g.getVertices(), f_outdegree_num)
        for nbr in nbrList:
            t = g.getVertex(nbr).getId()
            if g.getIndegree(t) < max_indegree_num:
                g.addEdge(f, t)
    if if_connected and not is_connected(g):
        g = create_graph(nodes_num, indegree_num, outdegree_num, name)
    return g

def connect_block(graph1, pointer_key, graph2):
    graph1.addPointer(pointer_key, graph2)
    graph2.Graph_name = graph1.getVertex(pointer_key).name
    return graph1, graph2

def create_graphs(indegree_num, outdegree_num, nodes_num = 1, graphs_num = 1):
    """
    Parameters
    ----------
    indegree_num : int
        max number of indegree in each graph.
    outdegree_num : int
        max number of outdegree in each graph.
    nodes_num : int, optional
        DESCRIPTION. The default is 1.
    graphs_num : int, optional
        number of graphs. The default is 1.
    Returns
    -------
    gs : list
        list of connected graphs.
    """
    gs = list()
    for i in range(graphs_num):
        g = create_graph(nodes_num, indegree_num, outdegree_num, name = chr(65+i))
        if i > 0:
            #select a random number of nodes to be ポインター
            g0 = random.choice(gs)
            v = g0.getVertex(random.randint(0, len(g0)))
            j = 0
            while(v.isPointer()):
                v = g0.getVertex(random.randint(0, len(g0)))
                j += 1
                if j >= 30: break
            connect_block(g0, v.id, g)
        gs.append(g)
    return gs

if __name__ == '__main__':
    #testing
    # g = create_graph(6, 3, 3, 'gA')
    # g2 = create_graph(6, 3, 3,'gB')
    # plot_graph(g, 'g')
    # show_details(g)

    # g3 = g.clone()
    # plot_graph(g3, 'g3')
    # show_details(g3)

    # connect_block(g, 2, g2)
    # plot_graph(g2, 'g2')

    # print(is_equal(g, g))
    # print(is_equal(g, g3))

    gs_0, gs_1, gs_2, gs_3, gs_4, gs_5, gs_6 = create_graphs(4, 4, 8, 7)

    for i in range(7):
        plot_graph(eval('gs_{}'.format(i)), eval('gs_{}'.format(i)).Graph_name)
        show_details(eval('gs_{}'.format(i)))
    #print(is_equal(gs_0, gs_0))