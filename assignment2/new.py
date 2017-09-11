from solver import *
L = load_items('data/ks_4_0')
items, item_count, capacity = L
best = ks_greedy(*L)
best = Best(best[0], list(best[1]))
root = KnapsackElement(best, L[0], value = 0, capacity= 11)

a = root.get_options()
aa = a.get_options() if a else None
aaa = aa.get_options() if aa else None
aaaa = aaa.get_options() if aaa else None
aaab = aaa.get_options() if aaa else None
aab = aa.get_options() if aa else None
aaba = aab.get_options() if aab else None
aabb = aab.get_options() if aab else None
ab = a.get_options() if a else None
aba = ab.get_options() if ab else None
abaa = aba.get_options() if aba else None
abab = aba.get_options() if aba else None
abb = ab.get_options() if ab else None
abba = abb.get_options() if abb else None
abbb = abb.get_options() if abb else None

digraph ="""
digraph A {
root -> a;
root-> b;
a -> aa;
aa -> aaa;
aaa -> aaaa;
aaa -> aaab;
aa -> aab;
aab -> aaba;
aab -> aabb;
a-> ab;
ab -> aba;
aba -> abaa;
aba -> abab;
ab -> abb;
abb -> abba;
abb -> abbb;

b -> ba;
ba -> baa;
baa -> baaa;
baa -> baab;
ba -> bab;
bab -> baba;
bab -> babb;
b-> bb;
bb -> bba;
bba -> bbaa;
bba -> bbab;
bb -> bbb;
bbb -> bbba;
bbb -> bbbb;
}
"""
b = root.get_options()
ba = b.get_options() if b else None
baa = ba.get_options() if ba else None
baaa = baa.get_options() if baa else None
baab = baa.get_options() if baa else None
bab = ba.get_options() if ba else None
baba = bab.get_options() if bab else None
babb = bab.get_options() if bab else None
bb = b.get_options() if b else None
bba = bb.get_options() if bb else None
bbaa = bba.get_options() if bba else None
bbab = bba.get_options() if bba else None
bbb = bb.get_options() if bb else None
bbba = bbb.get_options() if bbb else None
bbbb = bbb.get_options() if bbb else None

root.calculate_options = True

stack = [None]*(item_count+1)
stack[0] = root
pos = 0

while True :
    print('#'*(pos+1))
    assert pos >= 0 and pos <= item_count, "Pos is off the rails"
    if pos == item_count and stack[pos].is_better :
        best.set_better(stack[pos].value, (stack[i] for i in range(1,len(items)+1)))
        print("Nueva mejor marca", best)
        pos -= 1
        continue
    node = stack[pos].get_options()
    if pos == 0 and not node :
        # It's time to break the loop
        print("breaking the loop")
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
        
