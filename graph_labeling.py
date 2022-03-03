# -*- coding: utf-8 -*-
import argparse
from functools import reduce

from equality_checking import is_equal
from graph_creating import Vertex, Graph, create_graph, create_graphs
from tools import searching_cycle, saving_graph, show_details, plot_graph, is_connected
from tools import get_parent_nodes_key, get_child_nodes_key

def creating_all(num, labels = ['I', 'O', 'U']):
    #return all combination of three labels in a graph with node number num
    #I, O , U refer to in, out and undec
    return reduce(lambda x, y:[z0 + z1 for z0 in x for z1 in y], [labels] * num)

def labeling(graph, key, label):
    if label[key] == 'I':
        graph.setCondition(key, 'in')
    elif label[key] == 'O':
        graph.setCondition(key, 'out')
    elif label[key] == 'U':
        graph.setCondition(key, 'undec')
    else:
        pass

def position_labeling(graph, label):
    for key in graph.getVertices():
        labeling(graph, key, label)

def completeness_checking(graph, key)->bool:
    condition = graph.getCondition(key)
    parent_nodes_key = get_parent_nodes_key(graph, key)
    child_nodes_key = get_child_nodes_key(graph, key)
    if condition == 'in':
        for p_key in parent_nodes_key:
            p_condition = graph.getCondition(p_key)
            if p_condition != 'out':
                return False
        for c_key in child_nodes_key:
            c_condition = graph.getCondition(c_key)
            if c_condition != 'out':
                return False
    elif condition == 'out':
        flag = False # If the parent nodes include a 'in'
        for p_key in parent_nodes_key:
            p_condition = graph.getCondition(p_key)
            if p_condition == 'in':
                flag = True
        if not flag:
            return False
        for c_key in child_nodes_key:
            c_condition = graph.getCondition(c_key)
            if c_condition != 'in':
                return False
    return True

def weaker_checking(graph, key)->bool:
    condition = graph.getCondition(key)
    parent_nodes_key = get_parent_nodes_key(graph, key)
    child_nodes_key = get_child_nodes_key(graph, key)
    if condition == 'in':
        for p_key in parent_nodes_key:
            p_condition = graph.getCondition(p_key)
            if p_condition != 'out':
                return False
        for c_key in child_nodes_key:
            c_condition = graph.getCondition(c_key)
            if c_condition != 'out':
                return False
    elif condition == 'out':
        flag = False # If the parent nodes include a 'in'
        for p_key in parent_nodes_key:
            p_condition = graph.getCondition(p_key)
            if p_condition == 'in':
                flag = True
        if not flag:
            return False
    return True

def position_soundness_checking(graph, key)->bool:
    condition = graph.getCondition(key)
    if graph.getVertex(key).isPointer():
        for k_ in graph.getVertices():
            if graph.getVertex(k_).isPointer() and key != k_:
                if graph.getCondition(key) == graph.getCondition(k_):
                    if is_equal(graph.getVertex(key).childBlock, graph.getVertex(k_).childBlock):
                        return False
    if not graph.getVertex(key).isPointer():
        for k_ in graph.getVertices():
            if not graph.getVertex(k_).isPointer() and key != k_:
                if graph.getCondition(key) == graph.getCondition(k_):
                    if graph.getVertex(key).value == graph.getVertex(k_).value:
                        return False
    return True

def get_all_labels(graph, Completeness = True,
                 Weaker = True, Position_soundness = True):
    #return list of labels sequence fits such conditions
    all_labels = creating_all(len(graph))
    total_possibility = len(all_labels)
    possible_labeling = list()
    print('Start labeling:')
    for i in range(len(all_labels)):
        label = all_labels[i]
        position_labeling(graph, label)
        flag = True # if this is a valid labeling
        for key in graph.getVertices():
            if Completeness:
                if not completeness_checking(graph, key):
                    flag = False
                    break
            elif Weaker:
                if not weaker_checking(graph, key):
                    flag = False
                    break
            if Position_soundness:
                if not position_soundness_checking(graph, key):
                    flag = False
                    break
            if not flag:
                break
        if flag:
            possible_labeling.append(label)
        if i % 100000 == 0 and i>0:
            print('Finished labeling {:.2f}%  {} / {}'.format(i*100/total_possibility, i, total_possibility))
    print('Labeling finsihed!!!')
    return possible_labeling

def saving_all(graph, possible_labeling):
    for i in range(len(possible_labeling)):
        position_labeling(graph, possible_labeling[i])
        condition = []
        for key in graph.getVertices():
            condition.append(graph.getCondition(key))
        name = graph.Graph_name +'_' + str(i)+'.png'
        plot_graph(graph, path = 'plotting', name = name, condition = condition)
        name = g.Graph_name +'_' + str(i)+'.txt'
        saving_graph(g, name = name)

Completeness = True
Weaker = False
Position_soundness = False
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='test')

    parser.add_argument('--c', type=bool, default=True)
    parser.add_argument('--w', type=bool, default=True)
    parser.add_argument('--ps', type=bool, default=True)
    parser.add_argument('--nodes_num', type=int, default=6)
    parser.add_argument('--indegree_num', type=int, default=3)
    parser.add_argument('--outdegree_num', type=int, default=3)
    parser.add_argument('--name', type=str, default='testF')
    parser.add_argument('--if_connected', type=bool, default=False)

    args = parser.parse_args()
    # gs_0, gs_1, gs_2, gs_3, gs_4, gs_5, gs_6 = create_graphs(4, 4, 8, 7)

    # for i in range(7):
    #     plot_graph(eval('gs_{}'.format(i)), path = 'plotting')
    #     show_details(eval('gs_{}'.format(i)))
    # saving_graph(graph = gs_0, path = 'saving')

    g = create_graph(args.nodes_num, args.indegree_num, args.outdegree_num, \
                     args.name, args.if_connected)
    show_details(g)
    # plot_graph(g, path = 'plotting')

    # res = position_labeling(g, start_key = 0)
    # saving_graph(g)
    # plot_graph(g, path = 'plotting', condition=res)

    all_labels = get_all_labels(g, Completeness=args.c, Weaker=args.w, Position_soundness=args.ps)
    saving_all(g, all_labels)
    print(all_labels)
