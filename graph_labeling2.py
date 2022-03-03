# -*- coding: utf-8 -*-

# This file is Unfinished due to the difficulty of dealing with so many 
# posibility of different graph. I tried another method to label graphs.
# Please see it in file 'graph_labeling.py'!!!

from equality_checking import is_equal
from graph_creating import Vertex, Graph, create_graph, create_graphs
from tools import searching_cycle, saving_graph, show_details, plot_graph, is_connected
from tools import get_parent_nodes_key, get_child_nodes_key

def labeling_completeness(graph, key, undec = False, start_node = False):
    #'Completeness' condition
    node = graph.getVertex(key)
    possible_label = None
    if undec: #if node in cycle, then it could be undec
        node.condition = 'undec'
        return 'undec'
    if start_node:
        node.condition = 'in'
        return 'in'
    # checking each node pointing to the key node
    # the possible_label could still be None only if:
    # 1.numbers of nodes pointing to the key nodes > 0
    # 2.but none of them is labeled by 'in'
    # 3.and some of them not labeled by 'out'
    if graph.getIndegree(key) == 0:
        possible_label = 'in'
    elif graph.getIndegree(key) > 0:
        flag = True  #if the node's condition could be 'in'
        parent_nodes_key = get_parent_nodes_key(graph, key)
        for parent_node_key in parent_nodes_key:
            if graph.getCondition(parent_node_key) == 'in':
                possible_label = 'out'
                break
            elif graph.getCondition(parent_node_key) != 'out':
                flag = False
        if flag: # all b belongs to pred(b,a) are 'out'
            possible_label = 'in'
    # checking each node which the key node points to
    if graph.getOutdegree(key) > 0:
        child_nodes_key = get_child_nodes_key(graph, key)
        for child_node_key in child_nodes_key:
            if graph.getCondition(child_node_key) == 'in':
                # the key node should be 'out'
                if possible_label == 'in': # rules conflict
                    possible_label = 'undec'
                    break
                else:
                    possible_label = 'out'
            if graph.getCondition(child_node_key) == 'out':
                #check such child_node_key's other parent nodes
                parent_nodes_key = get_parent_nodes_key(graph, child_node_key)
                flag = True #if the key node's condition must be 'in'
                for parent_node_key in parent_nodes_key:
                    if parent_node_key != key:
                        if graph.getCondition(parent_node_key) == 'in':
                            flag = False
                        if graph.getCondition(parent_node_key) == None:
                            flag = False
                if flag and possible_label == 'out': # rules conflict
                    possible_label = 'undec'
                    break
                elif flag:
                    possible_label = 'in'
                    break
    node.condition = possible_label
    return possible_label

def labeling_weaker(graph, key, undec = False):
    #'Weaker' condition
    node = graph.getVertex(key)
    possible_label = None
    if undec: #if node in cycle, then it could be undec
        node.condition = 'undec'
        return 'undec'
    # checking each node pointing to the key node
    if graph.getIndegree(key) > 0:
        parent_nodes_key = get_parent_nodes_key(graph, key)
        for parent_node_key in parent_nodes_key:
            if graph.getCondition(parent_node_key) == 'in':
                possible_label = 'out'
                break
    # checking each node which the key node points to
    if graph.getOutdegree(key) > 0:
        child_nodes_key = get_child_nodes_key(graph, key)
        for child_node_key in child_nodes_key:
            if graph.getCondition(child_node_key) == 'in':
                possible_label = 'out'
            if graph.getCondition(child_node_key) == 'out':
                #check such child_node_key's other parent nodes
                parent_nodes_key = get_parent_nodes_key(graph, child_node_key)
                flag = True #if the key node's condition must be 'in'
                for parent_node_key in parent_nodes_key:
                    if parent_node_key != key:
                        if graph.getCondition(parent_node_key) == 'in':
                            flag = False
                        if graph.getCondition(parent_node_key) == None:
                            flag = False
                if flag and possible_label == 'out': # rules conflict
                    possible_label = 'undec'
                    break
                elif flag:
                    possible_label = 'in'
    node.condition = possible_label
    return possible_label

def labeling_position_soundness(graph, key, undec = False):
    #'Position soundness' condition
    pointers = list()
    non_pointers = list()
    for key in graph.getVertices():
        if graph.getVertex(key).isPointer():
            pointers.append(graph.getVertex(key))
        else:
            non_pointers.append(graph.getVertex(key))

def position_labeling(graph, start_key, undec = False,
                      Completeness = True, Weaker = False, Position_soundness = False):
    #clear all labels
    for key in graph.getVertices():
        graph.setCondition(key, label = None)

    if Completeness:
        labeled_key = list()
        labeled_key.append(start_key)
        if searching_cycle(graph, start_key) and undec == True:
            #in cycle, possibility of 'undec'
            label = labeling_completeness(graph, start_key, undec = True)
        else:
            label = labeling_completeness(graph, key = start_key, start_node = True)
            print('labeling node {} by {}'.format(start_key, label))
        while len(labeled_key) < len(graph):
            for edge in graph.getEdgesKey():
                if edge[0] in labeled_key and edge[1] not in labeled_key:
                    label = labeling_completeness(graph, edge[1])
                    if label:
                        labeled_key.append(edge[1])
                        print('labeling node {} by {}'.format(edge[1], label))
                    else:
                        print('node {} is unsure, skip labeling it'.format(edge[1]))
            for edge in graph.getEdgesKey():
                if edge[1] in labeled_key and edge[0] not in labeled_key:
                    label = labeling_completeness(graph, edge[0])
                    if label:
                        labeled_key.append(edge[0])
                        print('labeling node {} by {}'.format(edge[0], label))
                    else:
                        print('node {} is unsure, skip labeling it'.format(edge[0]))
    elif Weaker:
        labeled_key = list()
        labeled_key.append(start_key)
        if searching_cycle(graph, start_key) and undec == True:
            #in cycle, possibility of 'undec'
            labeling_weaker(graph, start_key, undec = True)
        else:
            labeling_weaker(graph, key = start_key, start_key = True)
        while len(labeled_key) < len(graph):
            for edge in graph.getEdgesKey():
                if edge[0] in labeled_key and edge[1] not in labeled_key:
                    label = labeling_weaker(graph, edge[1])
                    if label:
                        labeled_key.append(edge[1])
                        print('labeling node {} by {}'.format(edge[1], label))
                    else:
                        print('node {} is unsure, skip labeling it'.format(edge[1]))
            for edge in graph.getEdgesKey():
                if edge[1] in labeled_key and edge[0] not in labeled_key:
                    label = labeling_weaker(graph, edge[0])
                    if label:
                        labeled_key.append(edge[0])
                        print('labeling node {} by {}'.format(edge[0], label))
                    else:
                        print('node {} is unsure, skip labeling it'.format(edge[0]))

    res = list()
    for key in graph.getVertices():
        condition = graph.getVertex(key).condition
        res.append(condition)
    return res

def position_labeling_all(graph):
    #labeling and saving all posibility
    #return all possible labeling result
    possible_RES = list()
    i = 0
    for key in graph.getVertices():
        if searching_cycle(graph, key):
            res = position_labeling(graph, key, undec=True,
                                    Completeness=Completeness,
                                    Weaker = Weaker,
                                    Position_soundness = Position_soundness)
            if res not in possible_RES:
                possible_RES.append(res)
                name = g.Graph_name +'_' + str(i)+'.png'
                plot_graph(g, path = 'plotting', name = name, condition=res)
                name = g.Graph_name +'_' + str(i)+'.txt'
                saving_graph(g, name = name)
                i += 1
        res = position_labeling(graph, key,
                                Completeness=Completeness,
                                Weaker = Weaker,
                                Position_soundness = Position_soundness)
        if res not in possible_RES:
            possible_RES.append(res)
            name = g.Graph_name +'_' + str(i)+'.png'
            plot_graph(g, path = 'plotting', name = name, condition=res)
            name = g.Graph_name +'_' + str(i)+'.txt'
            saving_graph(g, name = name)
            i += 1
    return possible_RES

Completeness = True
Weaker = False
Position_soundness = False
if __name__ == '__main__':

    # gs_0, gs_1, gs_2, gs_3, gs_4, gs_5, gs_6 = create_graphs(4, 4, 8, 7)

    # for i in range(7):
    #     plot_graph(eval('gs_{}'.format(i)), path = 'plotting')
    #     show_details(eval('gs_{}'.format(i)))
    # saving_graph(graph = gs_0, path = 'saving')

    g = create_graph(nodes_num=7, indegree_num=3, outdegree_num=3, name='test')
    show_details(g)
    plot_graph(g, path = 'plotting')

    # res = position_labeling(g, start_key = 0)
    # saving_graph(g)
    # plot_graph(g, path = 'plotting', condition=res)

    all_res = position_labeling_all(g)
    print(all_res)
