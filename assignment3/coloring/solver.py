#!/usr/bin/python3 -i
# -*- coding: utf-8 -*-

from collections import defaultdict

class ColorSolution:
    def __init__(self, num_colors, nodes, edges) :
        self.num_colors = num_colors
        self.nodes = nodes
        self.edges = edges
        self.rainbow = set(range(num_colors))
        self.node_coloring = [None]*len(nodes)
    def __repr__(self) :
        return f'ColorSolution<{self.numcolors}, {str(self.node_coloring)}>'

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    nodes = defaultdict(set)
    for u, v in edges :
        nodes[u].add(v)
        nodes[v].add(u)

    print(nodes)
    # ordering the nodes by degree
    nodes_by_degree = sorted([ (len(vs), u) for u, vs in nodes.items() ], reverse = True)
    print(nodes_by_degree)
    # build a trivial solution
    # every node has its own color
    solution = range(0, node_count)

    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

