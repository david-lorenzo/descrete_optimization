#!/usr/bin/python3 -i
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict

class ColorSolution:
    def __init__(self, num_colors, nodes, edges) :
        self.num_colors = num_colors
        self.nodes = nodes
        self.edges = edges
        self.rainbow = set(range(num_colors))
        self.node_coloring = [None]*len(nodes)
        self.color_options = [None]*len(nodes)
        self.nodes_by_degree = [nid for _, nid in sorted([ (len(vs), u) for u, vs in nodes.items() ], reverse = True)]
        self.nbd_inverse = {nid: pos for pos, nid in enumerate(self.nodes_by_degree)}
        self.sol= None
        self.solved = False
        self._color_graph()
    def __repr__(self) :
        return f'ColorSolution<{self.num_colors}, {str(self.solution) if self.solved else None}>'
    def _get_opt_colors(self, pos) :
#        print('-'*10)
#        print('nodes_by_degree', self.nodes_by_degree)
#        print('nbd_inverse', [self.nbd_inverse[k] for k in range(len(self.nbd_inverse))])
#        print('pos', pos)
        nid = self.nodes_by_degree[pos]
#        print('nid', nid)
        neighbors_id = self.nodes[nid]
#        print('neighbors_id', neighbors_id)
        neighbors_pos = [self.nbd_inverse[nid] for nid in neighbors_id]
#        print('neighbors_pos', neighbors_pos)
        neighbors_colors = [self.node_coloring[i] for i in neighbors_pos if self.node_coloring[i]]
#        print("neighbors_colors", neighbors_colors)
        neighbors_colors = set(neighbors_colors)
#        print("neighbors_colors", neighbors_colors)
#        print("rainbow", sorted(list(self.rainbow)))
        possible_colors = sorted(list(self.rainbow - neighbors_colors))
#        print('possible_colors', possible_colors)
        return possible_colors
    def _color_graph(self) :
        # greedy_approach:
        # we start coloring the most connected vertex
        # after that we jump to the next most connected vertex and check available colors
        pos = 0 
        while True :
            assert 0 <= pos and pos < len(self.node_coloring), f'Bad index for position: {pos}'
            print('#'*(pos+1))
            if self.color_options[pos] == None :
                # load the possible colors and continue
                self.color_options[pos] = self._get_opt_colors(pos)
                continue
            if self.color_options[pos] == [] :
                # it's time to backtrack and try another color
                self.color_options[pos] = None
                self.node_coloring[pos] = None
                pos -= 1
                if pos == -1 :
                    # there is no solution
                    break
                continue
            if len(self.color_options[pos]) > 0 :
                self.node_coloring[pos] = self.color_options[pos].pop()
                pos += 1
                if pos >= len(self.node_coloring) :
                    self.solved = True
                    break
                continue
    @property
    def solution(self) :
        if not self.sol :
            self.sol = [None]*len(nodes)
            for n, c in zip(self.nodes_by_degree, self.node_coloring):
                self.sol[n] = c
        return self.sol.copy()

def check_solution(graph, solution) :
    for nid, color in enumerate(solution) :
        neighbors = graph[nid]
        neighbors_colors = [solution[nid] for nid in neighbors]
        print(f'{nid} {color}, {neighbors_colors}')
        if not all((color != neighbor_color for neighbor_color in neighbors_colors)) :
            return False
    return True

if __name__ == '__main__':
    file_location = sys.argv[1].strip() if len(sys.argv) > 1 else 'data/gc_20_1'
    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()

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

    # ordering the nodes by degree
    nodes_by_degree = sorted([ (len(vs), u) for u, vs in nodes.items() ], reverse = True)

    cs = ColorSolution(nodes_by_degree[0][0], nodes, edges)
    print(cs)
    cs1 = ColorSolution(2, nodes, edges)
    print(cs1)
    solution = cs1.solution
    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    print(output_data)

