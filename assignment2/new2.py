from solver import *

def original_order(items, flags) :
    inside = set((item.index for flag, item in zip(flags, items) if flag))
    return [1 if i in inside else 0 for i in range(len(items))]

def ks_bnb_dfs(list_items, item_count, capacity) :
    items = sorted(list_items, key = lambda x: x.density, reverse = True)
    best = ks_greedy(list_items, item_count, capacity)
    best = Best(best[0], list(best[1]))
    best.value = 100235
    best.value = 3966810
    root = KnapsackElement(best, items, value = 0, capacity= capacity)
    stack = [None]*(item_count+1)
    stack[0] = root
    pos = 0

    while True :
#        print('#'*(pos+1))
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

    
        
orig_items, item_count, capacity = load_items('data/ks_400_0')
value, output = ks_bnb_dfs(orig_items, item_count, capacity)

print(value)
print(' '.join(map(str, output)))
