# -*- coding: utf-8 -*-
import os
import networkx as nx
import matplotlib.pyplot as plt

def get_parent_nodes_key(graph, key):
    parent_nodes = []
    for edge in graph.getEdgesKey():
        if edge[1] == key:
            parent_nodes.append(edge[0])
    return parent_nodes

def get_child_nodes_key(graph, key):
    child_nodes = []
    for edge in graph.getEdgesKey():
        if edge[0] == key:
            child_nodes.append(edge[1])
    return child_nodes

def get_all_nodes(graph, nodes = None):
    #return list of all nodes in all position under such graph's position
    if not nodes:
        nodes = list()
    for key in graph.getVertices():
        node = graph.getVertex(key)
        nodes.append(node)
        if node.isPointer():
            nodes.extend(get_all_nodes(node.childBlock))
    return nodes

def searching_loop(graph, key)->bool:
    #judge if one node has a loop
    p_key = get_parent_nodes_key(graph, key)
    if key in p_key:
        return True
    else:
        return False

def searching_cycle(graph, key, start_key = None, searched_key = None)->bool:
    #judge if one node in the graph is in a cycle by DFS
    if searched_key == None:
        searched_key = list()
    if start_key == None:
        start_key = key
    edges = graph.getEdgesKey()
    if start_key in searched_key:
        return True
    for edge in edges:
        if edge[0] != key:
            continue
        if edge[0] == key and edge[1] not in searched_key:
            searched_key.append(edge[1])
            res = searching_cycle(graph, edge[1], start_key, searched_key)
            if res:
                return res
    if start_key == key:
        return False

def is_connected(graph, key = None, searched_key = None):
    if searched_key == None:
        searched_key = list()
    if key == None:
        key = 0
        searched_key.append(key)
    for edge in graph.getEdgesKey():
        if edge[0] == key and edge[1] not in searched_key:
            searched_key.append(edge[1])
            res = is_connected(graph, edge[1], searched_key)
        elif edge[1] == key and edge[0] not in searched_key:
            searched_key.append(edge[0])
            res = is_connected(graph, edge[0], searched_key)
    if len(searched_key) == len(graph):
        return True
    else:
        #print(searched_key)
        return False

def saving_graph(graph, path = 'saving', name = None, auto_sav_child = True):
    if not os.path.exists(path):
        os.makedirs(path)
    if name == None:
        name = graph.Graph_name+'.txt'
    saving_path = os.path.join(path, name)
    print('saving {} on path {}'.format(graph.Graph_name, saving_path))
    with open(saving_path, "w") as f:
        f.write('Graph name: ' + graph.Graph_name + '\n')
        f.write('Number of nodes: ' + str(graph.numVertices) + '\n')
        f.write('Names of nodes: ' + ','.join(graph.getVerticesNames()) + '\n')
        f.write('Conditions on a position: ' + \
                ','.join([v.condition for v in graph.vertList.values()]) + \
                '\n')
        f.write('Keys of pointers: ')
        flag = 1
        for key in graph.getVertices():
            if graph.getVertex(key).isPointer():
                if flag == 0: f.write(',')
                f.write(str(key))
                if flag == 1: flag = 0
        if flag == 1: f.write('None')
        f.write('\n')

        for edge in graph.getEdgesKey():
            f.write(str(edge) + '\n')
    f.close()
    if auto_sav_child:
        for key in graph.getVertices():
            if graph.getVertex(key).isPointer():
                saving_graph(graph.getVertex(key).childBlock, path)

def convert2networkx(g):
    G = nx.MultiDiGraph(name = g.Graph_name)
    G.add_nodes_from(g.getVerticesNames())
    G.add_edges_from(g.getEdges(), loop = True)
    return G

def plot_graph(graph, path = 'plotting', name = None ,condition = None):
    if not os.path.exists(path):
        os.makedirs(path)
    if name == None: name = graph.Graph_name+'.png'
    path = os.path.join(path, name)
    G = convert2networkx(graph)
    #pos = nx.spring_layout(G)
    pos = nx.circular_layout(G)
    plt.subplot()
    if condition != None:
        colors = []
        condition2colors = {'in': 'b', 'out': 'r', 'undec': 'y'}
        for label in condition:
            colors.append(condition2colors[label])
    else: colors = 'g'
    node_size = []
    for key in range(len(graph)):
        if searching_loop(graph, key):
            node_size.append(2000)
        else:
            node_size.append(1000)
    nx.draw(G, pos, with_labels = True, node_size = node_size, width=2.0,\
            node_color = colors)
    plt.title(graph.Graph_name)
    plt.show()
    plt.savefig(path)
    plt.close()
    print('plotting fig {}'.format(name))

def show_details(g):
    print('Graph name: {}'.format(g.Graph_name))
    print('Edges:', ' | '.join([str(i) for i in g.getEdgesKey()]))
    print('name indegree outdegree isPointer label value:')
    for v in range(len(g.getVertices())):
        print(g.getVertex(v).name, g.getIndegree(v), g.getOutdegree(v), \
              g.getVertex(v).isPointer(), g.getVertex(v).condition, \
              g.getVertex(v).value ,sep = ' | ')
