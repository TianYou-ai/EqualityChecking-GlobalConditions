# -*- coding: utf-8 -*-
from equality_checking import is_equal
from graph_creating import Vertex, Graph, create_graph, create_graphs
from tools import searching_cycle, saving_graph, show_details, plot_graph, is_connected

def labeling(graph, key, undec = False):
    node = graph.getVertex(key)
    if undec: #if node in cycle, then it could be undec
        node.condition = 'undec'

    #'Completeness' condition
    elif graph.getIndegree(key) == 0:
        node.condition = 'in'
        return 'in'
    elif graph.getIndegree(key) > 0:
        flag = True  #if the node's condition could be 'in'
        for edge in graph.getEdgesKey():
            if edge[1] == key and graph.getVertex(edge[0]).condition == 'in':
                node.condition = 'out'
                return 'out'
            elif edge[1] == key and graph.getVertex(edge[0]).condition != 'out':
                flag = False
        if flag:
            node.condition = 'in'
            return 'in'

    #numbers of b belongs to pred(b,a) > 0 but none of them is labeled
    #'Weaker' condition
    if graph.getOutdegree(key) > 0:
        flag = True #if the node's condition could be 'in'
        for edge in graph.getEdgesKey():
            if edge[0] == key and graph.getVertex(edge[1]).condition == 'in':
                node.condition = 'out'
                return 'out'
            if edge[0] == key and graph.getVertex(edge[1]).condition != 'out':
                flag = False
        if flag:
            node.condition = 'in'
            return 'in'

    #neither 'Completeness' nor 'Weaker' condition
    node.condition = 'undec'
    return 'undec'

def position_labeling(graph, start_key, undec = False):

    #clear all labels
    for key in graph.getVertices():
        graph.setCondition(key, label = None)

    labeled_key = list()
    labeled_key.append(start_key)

    if searching_cycle(graph, start_key) and undec == True:
        #in cycle, possibility of 'undec'
        labeling(graph, start_key, undec = True)
    else:
        labeling(graph, key = start_key)

    while len(labeled_key) < len(graph):
        for edge in graph.getEdgesKey():
            if edge[0] in labeled_key and edge[1] not in labeled_key:
                labeling(graph, edge[1])
                labeled_key.append(edge[1])
        for edge in graph.getEdgesKey():
            if edge[1] in labeled_key and edge[0] not in labeled_key:
                labeling(graph, edge[0])
                labeled_key.append(edge[0])
    res = list()
    for key in graph.getVertices():
        condition = graph.getVertex(key).condition
        res.append(condition)
    return res

def position_labeling_all(graph):
    possible_RES = list()
    i = 0
    for key in graph.getVertices():
        if searching_cycle(graph, key):
            res = position_labeling(graph, key, undec=True)
            if res not in possible_RES:
                possible_RES.append(res)
                name = g.Graph_name +'_' + str(i)+'.png'
                plot_graph(g, path = 'plotting', name = name, condition=res)
                name = g.Graph_name +'_' + str(i)+'.txt'
                saving_graph(g, name = name)
                i += 1
        res = position_labeling(graph, key)
        if res not in possible_RES:
            possible_RES.append(res)
            name = g.Graph_name +'_' + str(i)+'.png'
            plot_graph(g, path = 'plotting', name = name, condition=res)
            name = g.Graph_name +'_' + str(i)+'.txt'
            saving_graph(g, name = name)
            i += 1
    return possible_RES

if __name__ == '__main__':

    # gs_0, gs_1, gs_2, gs_3, gs_4, gs_5, gs_6 = create_graphs(4, 4, 8, 7)

    # for i in range(7):
    #     plot_graph(eval('gs_{}'.format(i)), path = 'plotting')
    #     show_details(eval('gs_{}'.format(i)))
    # saving_graph(graph = gs_0, path = 'saving')

    g = create_graph(nodes_num=8, indegree_num=3, outdegree_num=3, name='test')
    show_details(g)
    plot_graph(g, path = 'plotting')

    # res = position_labeling(g, start_key = 0)
    # saving_graph(g)
    # plot_graph(g, path = 'plotting', condition=res)

    all_res = position_labeling_all(g)
    print(all_res)
