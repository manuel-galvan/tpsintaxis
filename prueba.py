from anytree import Node, RenderTree
udo = Node("Udo")
marc = Node("Marc")
lian = Node("Lian", parent=marc)
print(RenderTree(udo))
Node('/Udo')
print(RenderTree(marc))
print(lian.is_root)
    

