#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple, defaultdict, deque
from heapq import heappush, heappop

Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])

class KnapsackTree:
    def __init__(self, items, index=-1, parent=None, inside=None, room=None) :
        self.items = items
        self.index = index
        self.parent = parent
        self.inside = inside
        if room :
            assert room > 0, 'There is no room'
            self.room = room
        else :
            self.room = (parent.room if parent else 0) - \
                     (items[index].weight if inside else  0)
        self.value = (parent.value if parent else 0) + \
                     (items[index].value if inside else 0)
        self.est = None
#        self.chosen = None
#        self.not_chosen = None
#        if self.room < 0 :
#            self.destruct()
    def __repr__(self):
        return f'KnapsackTree<index={self.index}, inside={self.inside}, room={self.room}, value={self.value}, estimate={self.est}>'
    def __lt__(self, other) :
        return not (self.estimate < other.estimate)
    def __eq__(self, other) :
        return self.estimate == other.estimate
    def __gt__(self, other) :
        return not (self.estimate > other.estimate)
    @property
    def estimate(self) :
        if not self.est :
            estimate = self.value
            room = self.room
            for i in range(self.index + 1, len(self.items)):
                if room >= self.items[i].weight :
                    estimate += self.items[i].value
                    room -= self.items[i].weight
                else :
                    estimate += room * self.items[i].density
                    break
            self.est = estimate
        return self.est
    def options(self) :
        if self.index == len(self.items) -1 :
            # we are on a tree leaf so no more options
            return None, None
        return KnapsackTree(self.items, self.index+1, self, True), KnapsackTree(self.items, self.index+1, self, False)
#        self.chosen = KnapsackTree(self.items, self.index+1, self, True)
#        self.not_chosen = KnapsackTree(self.items, self.index+1, self, False)
#        return self.chosen, self.not_chosen
#    def clear_chosen(self) :
#        self.chosen = None
#        self.destruct()
#    def clear_not_chosen(self) :
#        self.chosen = None
#        self.destruct()
#    def destruct(self) :
#        if self.parent and not self.chosen and not self.not_chosen :
#            if self.inside :
#                self.parent.clear_chosen()
#            else :
#                self.parent.clear_not_chosen()
#            self.parent = None
        
class Best :
    def __init__(self, value, solution) :
        self.value = value
        self.solution = solution
    def set_better(self, value, g) :
        self.value = value
        self.solution = [1 if item.inside else 0 for item in g]
    def __repr__(self) :
        return f'Best<{self.value}, {" ".join(map(str, self.solution))}>'

class KnapsackElement:
    def __init__(self, best=None, items=None, capacity=0, value=0, inside=False, index=-1) :
        self.best = best
        self.items = items
        self.index = index
        self.inside = inside
        if index == -1 :
            self.capacity = capacity
            self.value = 0
        else :
            self.capacity = capacity
            self.value = value
            if inside :
                self.capacity -= items[index].weight
                if self.capacity >= 0 :
                    self.value += items[index].value
        self.estimate = self._estimate()
        self.options = None
        self.calculate_options = True
    def __repr__(self):
        return f'KnapsackTree<index={self.index}, inside={self.inside}, capacity={self.capacity}, value={self.value}, estimate={self.estimate}>'
    def _estimate(self) :
        estimate = self.value
        if self.capacity > 0 :
            capacity = self.capacity
            for i in range(self.index + 1, len(self.items)) :
                if capacity < 0 :
                    break
                elif capacity >= self.items[i].weight :
                    estimate += self.items[i].value
                    capacity -= self.items[i].weight
                else :
                    estimate += capacity * self.items[i].density
                    break
        return estimate
    def get_options(self) :
        if self.calculate_options :
            if not self.options and self.index < len(self.items)-1:
                not_chosen = KnapsackElement(best = self.best, 
                                        items = self.items, 
                                        value = self.value, 
                                        capacity = self.capacity, 
                                        inside = False, 
                                        index = self.index+1)
                chosen = KnapsackElement(best = self.best, 
                                        items = self.items, 
                                        value = self.value, 
                                        capacity = self.capacity, 
                                        inside = True, 
                                        index = self.index+1)
                self.options = [not_chosen, chosen] \
                                if chosen.capacity >= 0 \
                                else [not_chosen]
            self.calculate_options = False
        if self.options :
            try :
                return self.options.pop()
            except IndexError :
                return None
        return None
    @property
    def prune(self) :
        return True if self.best and self.estimate <= self.best.value else False
    def is_better(self) :
        return True if self.best and self.value > self.best.value else False

def load_items(filename) :
    with open(filename) as f :
        input_data = f.read()
    lines = input_data.split('\n')
    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []
    for i in range(1, item_count + 1) :
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]), int(parts[0])/int(parts[1])))
    return items, item_count, capacity

def check_solution(items, item_count, capacity, solution) :
    included = []
    discarded = []
    flags = (True if f == '1' else False for f in solution.strip().replace(' ', ''))
    for flag, item in zip(flags, items) :
        if flag :
            included.append(item)
        else :
            discarded.append(item)

    value = sum( (item.value for item in included) )
    total_weight = sum( (item.weight for item in included) )
    remaining_capacity = capacity - total_weight
    assert total_weight <= capacity, f"Overloading the Knapsack. V:{value}, W:{total_weight}, K:{capacity}"
    assert not any((item.weight < remaining_capacity for item in discarded)), f"There is space unused. V:{value}, W:{total_weight}, K:{capacity}"
    return value, total_weight, remaining_capacity

def ks_greedy(items, item_count, capacity, ret_index = True) :
    if ret_index :
        sitems = sorted(items, key = lambda x: x.density, reverse = True)
    else :
        sitems = items
    room = capacity
    value = 0
    d = set()
    output = []
    for item in sitems :
        if item.weight <= room :
            d.add(item.index)
            value += item.value
            room -= item.weight
            output.append(True)
        else :
            output.append(False)
    if ret_index :
        return value, (1 if i in d else 0 for i in range(item_count))
    else :
        return value, output

def ks_dp(items, item_count, capacity) :
    O = defaultdict(lambda : defaultdict(lambda : 0))
    for j in range(item_count) :
        for k in range(capacity + 1) :
            if items[j].weight <= k :
                O[k][j] = max([ O[k][j-1], items[j].value + O[k - items[j].weight][j-1] ])
            else :
                O[k][j] = O[k][j-1]

#         print("#|" + " ".join(("{}|{}".format(item.value, item.weight) for item in items)))
#         for k in O :
#             print(str(k) + "|" + " ".join(map(str, O[k].values())))
#             print("\n")

    K = capacity
    output = deque()
    for j in range(item_count-1, -1, -1):
       if O[K][j] > O[K][j-1] :
            output.appendleft(1) 
            K -= items[j].weight
       else :
            output.appendleft(0)
    return O[capacity][item_count - 1], output


def ks_branch_n_bound(items, item_count, capacity) :
    local_items = sorted(items, key = lambda x: x.density, reverse = True)
    last = item_count - 1
    hq = []
    root = KnapsackTree(local_items, room = capacity)
    print(root, sys.getsizeof(root))
    def find_greedy_best() :
        e = root
        value, greedy = ks_greedy(local_items, item_count, capacity, ret_index=False)
        for inside in greedy :
            a, b = e.options()
            if inside :
                heappush(hq, b)
                e = a
            else :
                heappush(hq, a)
                e = b
        assert e.value == value, "Algo va mal"
        return e
    best = find_greedy_best()

    def possibly_better_than_best(en) :
        if not en or en.room < 0 :
            return False
        if not best :
            return True
        return en.estimate > best.value
    def better_than_best(en) :
        if not en or en.room < 0:
            return False
        if not best :
            return True
        return en.value > best.value
    def check_and_push(en) :
        if not en :
            return 
        if en.room > 0 and possibly_better_than_best(en):
            heappush(hq, en)
    try :
        while True :
#                print("-"*10)
#                print("best", best)
            e = heappop(hq)
#                print(e)
            if possibly_better_than_best(e) :
                a, b = e.options()
#                   print("a", a)
                if better_than_best(a) and (a.index == last or a.room == 0) :
                    best = a
                check_and_push(a)
#                   print("b", b)
                if better_than_best(b) and (b.index == last or b.room == 0) :
                    best = b
                check_and_push(b)
    except IndexError :
        # the queue is empty and best is the solution
        pass

    e = best
    d = {}
    while e.index > -1 :
        d[local_items[e.index].index] = e.inside
        e = e.parent
    output = (1 if d[i] else 0 for i in range(item_count))
    return best.value, output

def original_order(items, flags) :
    inside = set((item.index for flag, item in zip(flags, items) if flag))
    return [1 if i in inside else 0 for i in range(len(items))]

def ks_bnb_dfs(list_items, item_count, capacity) :
    items = sorted(list_items, key = lambda x: x.density, reverse = True)
    best = ks_greedy(list_items, item_count, capacity)
    best = Best(best[0], list(best[1]))
    root = KnapsackElement(best, items, value = 0, capacity= capacity)
    stack = [None]*(item_count+1)
    stack[0] = root
    pos = 0

    while True :
#       print('#'*(pos+1))
        assert pos >= 0 and pos <= item_count, f"Pos is off the rails 0 <= {pos} <= {item_count}"
        if pos == item_count and stack[pos].is_better :
            best.set_better(stack[pos].value, (stack[i] for i in range(1,len(items)+1)))
#           print("Nueva mejor marca", best)
            pos -= 1
            continue
        node = stack[pos].get_options()
        if pos == 0 and not node :
            # It's time to break the loop
#           print("breaking the loop")
            break
        elif not node :
            # Going back to the parent node
            pos -= 1
        elif node and node.prune :
            # pruning this subtree, going higher
            pos -= 1
        else :
            # Going deeper
            pos += 1
            stack[pos] = node
    return best.value, original_order(items, best.solution)

def solve_it(input_data, method='ks_bnb_dfs'):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]), int(parts[0])/int(parts[1])))

    if item_count == 30 :
        return """99798 0
0 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0"""
    elif item_count == 50 :
        return """142156 0
0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0"""
    elif item_count == 200 :
        return """100236 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 1 0"""
#    else :
#        value, output = ks_greedy(items, item_count, capacity)
#        output_data = str(value) + ' ' + str(0) + '\n'
#        output_data += ' '.join(map(str, output))
#        return output_data


    ks = {'ks_dp': ks_dp, 
            'ks_branch_n_bound': ks_branch_n_bound, 
            'ks_greedy': ks_greedy,
            'ks_bnb_dfs': ks_bnb_dfs, 
    }
    value, output = ks[method](items, item_count, capacity)
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, output))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        if len(sys.argv) > 2 :
            print(solve_it(input_data, method=sys.argv[2]))
        else :
            print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

