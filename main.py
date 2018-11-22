class NodeException(BaseException):
    pass

class Tree:
    def __init__(self):
        self.nodes = []

    def max_nesting_level(self) -> int:
        return max(len(node.get_nested_parents()) for node in self.nodes) + 1

    @staticmethod
    def print_tree(head:'Node', level:int=0) -> None:
        offset = '-'*level
        print(offset+head.name)
        for child in head.get_childs():
            Tree.print_tree(child, level=level+1)
    
    def get_root(self) -> 'Node' or None:
        return next(iter([node for node in self.nodes if not node.parent] or []), None)

class Node:
    def __init__(self, name: str, tree: Tree, parent:'Node'=None):
        self.name = name
       
        self.tree = tree
        self.tree.nodes.append(self)
        
        self.__parent = None
        self.parent = parent
    
    def __str__(self):
        return self.name

    def remove(self) -> None:
        if self.parent:
            for child in self.get_childs():
                child.parent = self.parent
        self.tree.nodes.remove(self)
        del self


    @property
    def parent(self) -> 'Node':
        return self.__parent

    @parent.setter
    def parent(self, value: 'Node'):
        if value in self.get_nested_childs():
            raise NodeException('Loop cached')
        self.__parent = value

    def get_nested_parents(self) -> list:
        parents = []
        if self.parent:
            parents = [*self.parent.get_nested_parents(), self.parent]
        return parents

    
    def get_childs(self) -> list:
        nodes = [node for node in self.tree.nodes if node.parent == self] 
        return nodes
    
    def get_nested_childs(self) -> list:
        nodes = self.get_childs()
        childs = nodes
        for node in nodes:
            node_childs = node.get_childs()
            if node_childs:
                childs.extend(node_childs)
        return childs


############### TESTING ###############


# Init tree
tree = Tree()
a = Node('1', tree)
b = Node('2', tree, a)
c = Node('3', tree, a)
d = Node('4', tree, c)
f = Node('5', tree, c)
g = Node('6', tree, c)
h = Node('7', tree, d)
i = Node('8', tree, f)
j = Node('9', tree, f)

# Print tree
tree.print_tree(a)

# Print childs for c:
print('Childs for 3 => '+' '.join([str(x) for x in c.get_childs()]))

# Print nested childs for c:
print('Nesed childs for 3 => '+' '.join([str(x) for x in c.get_nested_childs()]))

# Print parent for f:
print('Parent for 8 => %s' % j.parent)

# Print nested parents for f:
print('Nesed parents for 9 => '+' '.join([str(x) for x in j.get_nested_parents()]))

# Print max nesting level:
print('Max nesting level => '+ str(tree.max_nesting_level()))

# Get root of tree:
print('Root of tree => '+str(tree.get_root()))

# Remove node without removal anomaly (connect children with self parent as their parent)
c.remove()

# # Try to loop tree
# a.parent = j

# # Check relations
# print('\n'.join(['%s - %s' % (str(x), str(x.parent or '')) for x in tree.nodes]))
