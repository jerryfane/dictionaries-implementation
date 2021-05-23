from RedBlackTree import *


class MapRBTree(RedBlackTree):
    
    def add(self, value, value_value=None):
        if not self.root:
            self.root = Node(value, color=BLACK, parent=None, 
                             left=self.NIL_LEAF, right=self.NIL_LEAF, value_value=value_value)
            self.count += 1
            return
        parent, node_dir = self._find_parent(value)
        if node_dir is None:
            return  # value is in the tree
        new_node = Node(value=value, color=RED, parent=parent, 
                        left=self.NIL_LEAF, right=self.NIL_LEAF, value_value=value_value)
        if node_dir == 'L':
            parent.left = new_node
        else:
            parent.right = new_node

        self._try_rebalance(new_node)
        self.count += 1
    
    def get(self, value):
        return self.find_node(value).value_value
    
    def keys(self, root):
        #in-order trasversal
        if root == None:
            return []

        left_list = self.keys(root.left)
        right_list = self.keys(root.right)
        return left_list + [root.value] + right_list 
    