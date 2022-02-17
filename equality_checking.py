# -*- coding: utf-8 -*-
def find_matched_id(key, matched_key):
    for key1, key2 in matched_key:
        if key == key1:
            return key2

def find_matched_id2(key, matched_key):
    for key1, key2 in matched_key:
        if key == key2:
            return key1

def is_equal(graph1, graph2, matched_key = None):
    #check g1&g2 if they follow the Equality (recurvise)
    if len(graph1) != len(graph2):
        return False
    if len(graph1.getEdges()) != len(graph2.getEdges()):
        return False
    if matched_key == None:
        matched_key = list()
    if len(matched_key) == len(graph1):
        #check all edges in g1 could map on g2
        edges = graph1.getEdgesKey()
        for edge in edges:
            key2f = find_matched_id(edge[0], matched_key)
            key2t = find_matched_id(edge[1], matched_key)
            if (key2f, key2t) not in graph2.getEdgesKey():
                return False
        #check all edges in graph2 could map on graph1
        edges = graph2.getEdgesKey()
        for edge in edges:
            key1f = find_matched_id2(edge[0], matched_key)
            key1t = find_matched_id2(edge[1], matched_key)
            if (key1f, key1t) not in graph1.getEdgesKey():
                return False
        return True
    for key1 in graph1.getVertices():
        #print(key1, matched_key)
        if key1 in map((lambda x: x[0]), matched_key):
            continue
        indegree1 = graph1.getIndegree(key1)
        outdegree1 = graph1.getOutdegree(key1)
        possible_vertkey = list()
        for key2 in graph2.getVertices():
            if key2 in map((lambda x: x[1]), matched_key):
                continue
            indegree2 = graph2.getIndegree(key2)
            outdegree2 = graph2.getOutdegree(key2)
            if indegree1 == indegree2 and outdegree1 == outdegree2:
                possible_vertkey.append(key2)
        if len(possible_vertkey) == 0:
            return False
        for key2 in possible_vertkey:
            #print(possible_vertkey)
            if graph1.getVertex(key1).isPointer() and graph2.getVertex(key2).isPointer():
                block1 = graph1.getVertex(key1).childBlock
                block2 = graph2.getVertex(key1).childBlock
                res = is_equal(block1, block2)
                if not res:
                    continue
            new_matched_key = matched_key.copy()
            new_matched_key.append((key1, key2))
            res = is_equal(graph1, graph2, new_matched_key)
            if not res:
                continue
            else:
                return res
    return False

def is_condition(graph):
    #search all of the pointers in such graph
    #check whether each pair of them fit the condition
    #return False when some pair of pointers don't fit condition
    pointers = list()
    for key in graph.getVertices():
        if graph.getVertex(key).isPointer():
            pointers.append(graph.getVertex(key))
    if len(pointers)>=2:
        for i in range(len(pointers)-1):
            for j in range(i+1, len(pointers)):
                g1 = graph.getVertex(i).childBlock
                g2 = graph.getVertex(j).childBlock
                if not is_equal(g1, g2):
                    return False
    return True