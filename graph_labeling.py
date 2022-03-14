# -*- coding: utf-8 -*-
import os
import argparse
from functools import reduce

from equality_checking import is_equal
from graph_creating import Vertex, Graph, create_graph, create_graphs
from tools import searching_cycle, saving_graph, show_details, plot_graph, is_connected
from tools import get_parent_nodes_key, get_child_nodes_key, get_all_nodes

def creating_all(num, labels = ['I', 'O', 'U']):
    #return all combination of three labels in a graph with node number num
    #I, O , U refer to in, out and undec
    return reduce(lambda x, y:[z0 + z1 for z0 in x for z1 in y], [labels] * num)

def labeling(graph, key, label, label_key = None):
    if label_key is None:
        label_key = key
    if label[label_key] == 'I':
        graph.setCondition(key, 'in')
    elif label[label_key] == 'O':
        graph.setCondition(key, 'out')
    elif label[label_key] == 'U':
        graph.setCondition(key, 'undec')
    else:
        pass

def position_labeling(graph, label):
    for key in graph.getVertices():
        labeling(graph, key, label)

def global_labeling(root_graph, labels, nodes):
    for i in range(len(nodes)):
        labeling(nodes[i].Block, nodes[i].id, labels, i)

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
                if is_equal(graph.getVertex(key).childBlock, graph.getVertex(k_).childBlock):
                    if condition == 'in' and graph.getVertex(k_).condition == 'out':
                        return False
                    if condition == 'out' and graph.getVertex(k_).condition == 'in':
                        return False
    if not graph.getVertex(key).isPointer():
        for k_ in graph.getVertices():
            if not graph.getVertex(k_).isPointer() and key != k_:
                if graph.getVertex(key).value == graph.getVertex(k_).value:
                    if condition == 'in' and graph.getVertex(k_).condition == 'out':
                        return False
                    if condition == 'out' and graph.getVertex(k_).condition == 'in':
                        return False
    return True

def stronger_position_soundness_checking(graph, key)->bool:
    condition = graph.getCondition(key)
    is_pointer = graph.getVertex(key).isPointer()
    for k_ in graph.getVertices():
        equal = False # if the two nodes are equal
        if key == k_:
            continue
        if is_pointer == graph.getVertex(k_).isPointer():
            if is_pointer and is_equal(graph.getVertex(key).childBlock, graph.getVertex(k_).childBlock):
                equal = True
            if not is_pointer and graph.getVertex(key).value == graph.getVertex(k_).value:
                equal = True
        if equal and graph.getCondition(k_) != condition:
            return False
    return True

def coherence_checking(graph, key, root_graph)->bool:
    node = graph.getVertex(key)
    nodes = get_all_nodes(root_graph)
    for node_ in nodes:
        equal = False # if the two nodes are equal
        if node_ == node:
            continue
        if node.Block != node_.Block:
            F = list()
            if is_equal(node.Block, node_.Block, matched_key = F):
                if (node.id, node_.id) in F:
                    equal = True
        else:
            if node.value == node_.value:
                equal = True
        if equal:
            if node.condition == 'in' and node_.condition == 'out':
                return False
            if node.condition == 'out' and node_.condition == 'in':
                return False
    return True

def stronger_coherence_checking(graph, key, root_graph)->bool:
    node = graph.getVertex(key)
    nodes = get_all_nodes(root_graph)
    for node_ in nodes:
        equal = False # if the two nodes are equal
        if node_ == node:
            continue
        if node.Block != node_.Block:
            F = list()
            if is_equal(node.Block, node_.Block, matched_key = F):
                if (node.id, node_.id) in F:
                    equal = True
        else:
            if node.value == node_.value:
                equal = True
        if equal and node.condition != node_.condition:
            return False
    return True

def logal_checking(graph, key, Completeness, Weaker,
                   Position_soundness, Stronger_position_soundness):
    node = graph.getVertex(key)
    for key in graph.getVertices():
        node_ = graph.getVertex(key)
        if node == node_:
            continue
        if Completeness:
            if not completeness_checking(graph, key):
                return False
        if Weaker:
            if not weaker_checking(graph, key):
                return False
        if Position_soundness:
            if not position_soundness_checking(graph, key):
                return False
        if Stronger_position_soundness:
            if not stronger_position_soundness_checking(graph, key):
                return False
    return True

def get_all_labels(graph, Completeness = True, Weaker = True,
                   Position_soundness = True, Stronger_position_soundness = True):
    #return list of labels sequence fits such conditions
    all_labels = creating_all(len(graph))
    total_possibility = len(all_labels)
    possible_labeling = list()
    print('Start labeling:')
    for i in range(len(all_labels)):
        labels = all_labels[i]
        position_labeling(graph, labels)
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
            if Stronger_position_soundness:
                if not stronger_position_soundness_checking(graph, key):
                    flag = False
                    break
            if not flag:
                break
        if flag:
            possible_labeling.append(labels)
        if i % 100000 == 0 and i>0:
            print('Finished labeling {:.2f}%  {} / {}'.format(i*100/total_possibility, i, total_possibility))
    print('Labeling finsihed!!!')
    return possible_labeling

def get_all_global_labels(root_graph, Coherence, Stronger_coherence,
                          Logal, Completeness = False, Weaker = False,
                          Position_soundness = False,
                          Stronger_position_soundness = False):
    nodes = get_all_nodes(root_graph)
    all_labels = creating_all(len(nodes))
    total_possibility = len(all_labels)
    possible_labeling = list()
    print('Start labeling:')
    for i in range(len(all_labels)):
        labels = all_labels[i]
        global_labeling(root_graph, labels, nodes)
        flag = True # if this is a valid labeling
        for node in nodes:
            graph = node.Block
            key = node.id
            if Coherence:
                if not coherence_checking(graph, key, root_graph):
                    flag = False
                    break
            if Stronger_coherence:
                if not stronger_coherence_checking(graph, key, root_graph):
                    flag = False
                    break
            if Logal:
                if not logal_checking(graph, key, Completeness, Weaker, Position_soundness, Stronger_position_soundness):
                    flag = False
                    break
        if flag:
            possible_labeling.append(labels)
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
        name = graph.Graph_name +'_' + str(i)+'.txt'
        saving_graph(graph, name = name)

def saving_all_global(root_graph, possible_labeling, path):
    nodes = get_all_nodes(root_graph)
    graphs = list()
    for node in nodes:
        if node.Block not in graphs:
            graphs.append(node.Block)
    i = -1
    for labels in possible_labeling:
        i += 1
        path_ = os.path.join(path, 'possibility_{}'.format(i))
        if not os.path.exists(path_):
            os.makedirs(path_)
        global_labeling(root_graph, labels, nodes)
        for graph in graphs:
            condition = []
            for key in graph.getVertices():
                condition.append(graph.getCondition(key))
            name = graph.Graph_name +'_possibility_' + str(i)+'.png'
            plot_graph(graph, path = path_, name = name, condition = condition)
            name = graph.Graph_name +'_possibility_' + str(i)+'.txt'
            saving_graph(graph, name = name, path = path_, auto_sav_child=False)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='test')

    parser.add_argument('--c', type=bool, default=False)
    parser.add_argument('--w', type=bool, default=True)
    parser.add_argument('--ps', type=bool, default=True)
    parser.add_argument('--sps', type=bool, default=True)
    parser.add_argument('--co', type=bool, default=True)
    parser.add_argument('--sco', type=bool, default=True)
    parser.add_argument('--l', type=bool, default=True)
    parser.add_argument('--nodes_num', type=int, default=4)
    parser.add_argument('--graphs_num', type=int, default=4)
    parser.add_argument('--indegree_num', type=int, default=2)
    parser.add_argument('--outdegree_num', type=int, default=2)
    parser.add_argument('--name', type=str, default='testG')
    parser.add_argument('--if_connected', type=bool, default=False)
    parser.add_argument('--path_name', type=str, default='test_global_1')

    args = parser.parse_args()
    # gs_0, gs_1, gs_2, gs_3, gs_4, gs_5, gs_6 = create_graphs(4, 4, 8, 7)

    # for i in range(7):
    #     plot_graph(eval('gs_{}'.format(i)), path = 'plotting')
    #     show_details(eval('gs_{}'.format(i)))
    # saving_graph(graph = gs_0, path = 'saving')

    # g = create_graph(args.nodes_num, args.indegree_num, args.outdegree_num, \
    #                  args.name, args.if_connected)
    # show_details(g)

    # res = position_labeling(g, start_key = 0)
    # saving_graph(g)
    # plot_graph(g, path = 'plotting', condition=res)

    # all_labels = get_all_labels(g, Completeness=args.c, Weaker=args.w,
    #                             Position_soundness=args.ps,
    #                             Stronger_position_soundness=args.sps)
    # saving_all(g, all_labels)
    # print(all_labels)
    graphs = create_graphs(indegree_num=args.indegree_num,
                           outdegree_num=args.outdegree_num,
                           nodes_num = args.nodes_num,
                           graphs_num = args.graphs_num,
                           if_connected = args.if_connected)
    root_graph = graphs[0]
    for graph in graphs:
        show_details(graph)
    possible_labeling = get_all_global_labels(root_graph, Coherence=args.co,
                                        Stronger_coherence=args.sco,
                                        Logal=args.l,
                                        Completeness=args.c,
                                        Weaker=args.w,
                                        Position_soundness=args.ps,
                                        Stronger_position_soundness=args.sps)
    saving_all_global(root_graph, possible_labeling, path = args.path_name)
