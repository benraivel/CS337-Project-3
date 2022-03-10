# CS337 Project 3
# Ben Raivel

# Implements RBNode and RBTree classes

from colorama import Fore, Back, Style
from random import shuffle

class RBNode:
    '''
    RBTree compatible node
    '''

    def __init__(self, key, value = None):
        '''
        creates node with key, color, empty attributes for parent and children nodes
        '''
        # node key
        self.key = key

        # value (a process object)
        self.value = value

        # node color (initially black)
        self.red = False

        # parent, children 'pointers'
        self.parent = None
        self.lchild = None
        self.rchild = None

    # Setters and Getters
    def get_key(self):
        return self.key

    def set_key(self, key):
        self.key = key

    def get_val(self):
        return self.value

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_lchild(self):
        return self.lchild

    def set_lchild(self, child):
        self.lchild = child

    def get_rchild(self):
        return self.rchild

    def set_rchild(self, child):
        self.rchild = child

    def is_red(self):
        return self.red

    def is_black(self):
        return not self.red

    def set_red(self):
        self.red = True

    def set_black(self):
        self.red = False
    
    def is_left(self):
        return self == self.parent.get_lchild()

    # specialty uncle getter
    def get_uncle(self):

        try:
            # if node is from a left parent
            if self.get_parent().get_parent().get_lchild() == self.get_parent():
                
                # uncle is grandparent's right child
                return self.get_parent().get_parent().get_rchild()
            
            else:
                # uncle is grandparent's left child
                return self.get_parent().get_parent().get_lchild()

        except:
            # problem fetching uncle
            return None


class RBTree:
    '''
    Red-Black Tree implementation
    '''

    def __init__(self):
        '''
        creates nil node, root and min_vruntime attributes
        '''
        # create nil node
        self.nil = RBNode(0, None)

        # set nil's attributes to itself
        self.nil.set_lchild(self.nil)
        self.nil.set_rchild(self.nil)
        self.nil.set_parent(self.nil)

        # set root to nil
        self.root = self.nil

        # set min_vruntime to root
        self.min_vruntime = None

        # size starts at 0
        self.size = 0

    def __len__(self):
        return self.size

    def insert(self, key, value = None):
        '''
        adds a node with key and optional value to the tree
        '''
        # create new node with value
        new_node = RBNode(key, value)

        if self.min_vruntime == None:
            self.min_vruntime = new_node

        # if the value of the new node is less than min_vruntime's key
        if key <= self.min_vruntime.get_key():

            # new node becomes min_vruntime
            self.min_vruntime = new_node

        # node 'pointers' to traverse the tree
        current_node = self.root
        prev_node = self.nil

        # traverse to find location to insert node
        while current_node != self.nil:

            # set prev to current
            prev_node = current_node

            # compare key of new node key of current
            if new_node.get_key() < current_node.get_key():

                # set current to be its left child
                current_node = current_node.get_lchild()

            # if new > current
            else:
                # set current to be its right child
                current_node = current_node.get_rchild()
        
        # location found, set new node's parent
        new_node.set_parent(prev_node)

        # special case: empty tree
        if prev_node == self.nil:

            # set root to new node
            self.root = new_node

        # otherwise compare new node's key to its parent
        else:

            # new node is parent's left child
            if new_node.get_key() < prev_node.get_key():
                prev_node.set_lchild(new_node)

            # otherwise new node is parent's right child
            else:
                prev_node.set_rchild(new_node)

        # set new node's child 'pointers' to nil
        new_node.set_lchild(self.nil)
        new_node.set_rchild(self.nil)

        # color node red
        new_node.set_red()

        # fix tree
        self.fix_insert(new_node)

        # increment size
        self.size += 1

    def fix_insert(self, node):
        '''
        repairs the tree to follow rules
        '''
        # loop while node's parent is red
        while node.get_parent().is_red():
            
            # get node's uncle
            uncle = node.get_uncle()

            # case 1
            if uncle.is_red():

                # color parent black
                node.get_parent().set_black()

                # color uncle black
                uncle.set_black()

                # color grandparent red
                node.get_parent().get_parent().set_red()

                # set node to be it's grandparent
                node = node.get_parent().get_parent()

            else:
                # check whether node/parent is a right/left child
                node_is_lchild = node.get_parent().get_lchild() == node
                node_is_rchild = node.get_parent().get_rchild() == node 
                parent_is_lchild = node.get_parent().get_parent().get_lchild() == node.get_parent
                parent_is_rchild = node.get_parent().get_parent().get_rchild() == node.get_parent
                
                # triangle pointing right
                if node_is_lchild and parent_is_rchild:
                    node = node.get_parent()
                    self.rotate_l(node.get_parent())

                # triangle pointing left
                elif node_is_rchild and parent_is_lchild:
                    node = node.get_parent()
                    self.rotate_r(node.get_parent())
                
                # color parent black
                node.get_parent().set_black()

                # color grandparent red
                node.get_parent().get_parent().set_red()

                # rotate grandparent
                if node_is_lchild:
                    self.rotate_r(node.get_parent().get_parent())
                elif node_is_rchild:
                    self.rotate_l(node.get_parent().get_parent())

        # color root black
        self.root.set_black()

    def remove(self, key=None, node=None):
        '''
        removes node (skipping O(log(n)) get method
        '''
        # if no node is provided
        if node is None:

            # if no key is provided
            if key is None:
                
                return None
            
            else: # get the node matching key
                node = self.get(key)

        # if min_vruntime is being removed
        if node == self.min_vruntime:

            if node.get_parent() == self.nil:
                self.min_vruntime = None

            elif node.get_rchild() == self.nil:
                self.min_vruntime = node.get_parent()
            else:
                self.min_vruntime = node.get_rchild()

        # get the value associated with node 
        val = node.get_val()

        # temp variables to hold node and it's color
        temp = node
        temp_red = temp.is_red()


        if node.get_lchild() == self.nil:
            
            temp2 = node.get_rchild()
            self.transplant(node, node.get_rchild())

        elif node.get_rchild() == self.nil:

            temp2 = node.get_lchild()
            self.transplant(node, node.get_lchild())

        else:
            temp = self.relocate_min(node.get_rchild())
            temp_red = temp.is_red()
            temp2 = temp.get_rchild()

            if temp.get_parent() == node:

                temp2.set_parent(temp)

            else:
                self.transplant(temp, temp.get_rchild())
                temp.set_rchild(node.get_rchild())
                temp.get_rchild().set_parent(temp)

            self.transplant(node, temp)
            temp.set_lchild(node.get_lchild())
            temp.get_lchild().set_parent(temp)

            if node.is_red():
                temp.set_red()
            else:
                temp.set_black()
        
        # if temp is black tree needs repair
        if not temp_red:

            # call fixup method
            self.fix_remove(temp2)
        
        # decrement size
        self.size -= 1

        return val

    def fix_remove(self, node):
        '''
        fixes the tree after removing a node
        '''
        # loop while node is non-root and doubly black
        while node != self.root and node.is_black():

            # TWO SYMMETRICAL SITUATIONS:
            # ===========================
            #   1 - NODE IS A LEFT CHILD:
            # ---------------------------
            if node.is_left():

                # sibling is parent's right child
                sibling = node.get_parent().get_rchild()

                # case 1: sibling is red
                if sibling.is_red():

                    sibling.set_black()                 # case 1
                    sibling.get_parent().set_black()    # case 1
                    self.rotate_l(node.get_parent())    # case 1

                    sibling = node.get_parent().get_rchild() # now have case 2, 3, or 4

                # case 2: both children are black
                if sibling.get_lchild().is_black() and sibling.get_rchild().is_black():

                    sibling.set_red()   # case 2

                    node = node.get_parent() # now have case 3 or 4
                
                else:
                    # case 3: sibling's right child is red, left child is black
                    if sibling.get_rchild().is_black():

                        sibling.get_lchild().set_black()    # case 3
                        sibling.set_red()                   # case 3
                        self.rotate_r(sibling)              # case 3

                        sibling = node.get_parent().get_rchild() # now have case 4

                    # case 4: sibling's right child is red
                    # recolor sibling to match node's parent
                    if node.get_parent().is_red(): sibling.set_red()
                    else: sibling.set_black()

                    node.get_parent().set_black()       # case 4
                    sibling.get_rchild().set_black()    # case 4
                    self.rotate_l(node.get_parent())    # case 4

                    node = self.root

            # ============================
            #   2 - NODE IS A RIGHT CHILD:
            # ----------------------------
            else:

                # sibling is parent's left child
                sibling = node.get_parent().get_lchild()

                # case 1: sibling is red
                if sibling.is_red():

                    sibling.set_black()                 # case 1
                    sibling.get_parent().set_black()    # case 1
                    self.rotate_r(node.get_parent())    # case 1

                    sibling = node.get_parent().get_lchild() # now have case 2, 3, or 4

                # case 2: both children are black
                if sibling.get_lchild().is_black() and sibling.get_rchild().is_black():

                    sibling.set_red()   # case 2

                    node = node.get_parent() # now have case 3 or 4
                
                else:
                    # case 3: 
                    if sibling.get_lchild().is_black():

                        sibling.get_rchild().set_black()
                        sibling.set_red()
                        self.rotate_l(sibling)

                        sibling = node.get_parent().get_rchild()

                    # case 4
                    if node.get_parent().is_red(): sibling.set_red()
                    else: sibling.set_black()

                    node.get_parent().set_black()
                    sibling.get_lchild().set_black()
                    self.rotate_r(node.get_parent())

                    node = self.root

        # color node black
        node.set_black()

    def transplant(self, n1, n2):
        '''
        replace the subtree of n1 with that of n2
        '''
        # special case: n1 is root
        if n1.get_parent() == self.nil:
            self.root = n2
        
        # if n1 is a left child
        elif n1.is_left():
            n1.get_parent().set_lchild(n2)

        else: # n2 is a right child
            n1.get_parent().set_rchild(n2)
        
        # n1's parent becomes n2's parent
        n2.set_parent(n1.get_parent())

    def rotate_l(self, node):
        '''
        performs left rotation
        '''
        # get right child of node
        pivot = node.get_rchild()

        # set node's right child attribute to be pivot's left child node
        node.set_rchild(pivot.get_lchild())

        # set pivot's left child's parent attribute to be node
        pivot.get_lchild().set_parent(node)

        # pivot's parent becomes node's parent
        pivot.set_parent(node.get_parent())

        # if node was root
        if node.get_parent() == self.nil:

            # pivot becomes root
            self.root = pivot

        # otherwise
        else:

            # if node was a left child
            if node == node.get_parent().get_lchild():
                
                # pivot becomes left child of node's parent
                node.get_parent().set_lchild(pivot)
            
            # otherwise node was a right child
            else:

                # pivot becomes right child of node's parent
                node.get_parent().set_rchild(pivot)

        pivot.set_lchild(node)
        node.set_parent(pivot)

    def rotate_r(self, node):
        '''
        performs right rotation
        '''
        # get left child of node
        pivot = node.get_lchild()

        # set node's left child to be pivot's right child
        node.set_lchild(pivot.get_rchild())

        # set pivot's right child's parent to be node
        pivot.get_rchild().set_parent(node)

        # set pivot's parent to be node's parent
        pivot.set_parent(node.get_parent())

        # if parent is nil
        if node.get_parent() == self.nil:

            # pivot is root
            self.root = pivot
        
        # otherwise set p parent's child
        else:

            # if node was a left child
            if node == node.get_parent().get_lchild():

                # pivot is parent's left child 
                node.get_parent().set_lchild(pivot)

            # otherwise
            else:

                # pivot is parent's right child 
                node.get_parent().set_rchild(pivot)

        # set pivot's right child to node
        pivot.set_rchild(node)

        # set node's parent to pivot
        node.set_parent(pivot)

    def get(self, key, node = None):
        '''
        - gets node with key
        - specify node for recursive call
        '''
        # on first call
        if node is None:

            # set node to be root
            node = self.root
        
        # if a nil node has been reached
        elif node is self.nil:
            
            # key not found in tree
            return None
        
        # if node matches the given key
        if key == node.get_key():
            
            # node found!
            return node 

        # if key would be on node's left
        elif key < node.get_key():
            
            # call get recursivley, passing in node's left child
            return self.get(key, node.get_lchild())
        
        else: # key would be on node's right
            return self.get(key, node.get_rchild())

    def get_min(self):
        '''
        gets the minimum
        '''
        if self.min_vruntime == None and self.size > 0:
            self.min_vruntime = self.relocate_min()
        return self.min_vruntime

    def relocate_min(self, node = None):
        if node == None:
            node = self.root
        
        if node.get_lchild() == self.nil:
            return node
        else:
            return self.relocate_min(node=node.get_lchild())

    def print_tree(self):
        '''
        print the full tree by calling 
        '''
        # loop up to height of root
        for i in range(self.height(self.root)):

            # print spaces
            for j in range(int((2**(self.height(self.root)+1))/2**(i+1))):
                print(' ', end='')
            
            # call print level 
            self.print_level(self.root, i, i)

            # print new line
            print('\n')

    def print_level(self, root, level, i):
        # at leaves
        if root == self.nil:
            for j in range(int((2**(self.height(self.root)+1))/2**(i))):
                print(' ', end='')
            if root.get_parent() == self.nil:
                return

        # level has been reached
        if level == 0:

            # print red nodes
            if root.is_red():

                # print key in red
                print(Fore.RED + str(root.get_key()) + Style.RESET_ALL, end = '')
                
                for j in range(int((2**(self.height(self.root) + 1))/2**(i))):
                    print(' ', end='') 
            
            # print non-nil black nodes
            elif root != self.nil:

                # print key
                print(str(root.get_key()), end = '')

                for j in range(int((2**(self.height(self.root) + 1))/2**(i))):
                    print(' ', end='')

        # level has not been reached
        elif level > 0:

            self.print_level(root.get_lchild(), level-1, i)
            self.print_level(root.get_rchild(), level-1, i)

    def height(self, node):
        '''
        returns height of tree rooted at node
        '''
        # if node is nil height is 0
        if node == self.nil:
            return 0
        
        # otherwise recursivley call height method
        else:
            height_lsubtree = self.height(node.get_lchild())
            height_rsubtree = self.height(node.get_rchild())

        # return the greater subtree height + 1
        if height_lsubtree > height_rsubtree:
            return height_lsubtree + 1
        else:
            return height_rsubtree + 1

    def get_size(self):
        return self.size


def test1():
    testtree = RBTree()

    for i in range(1, 20):
        testtree.insert(i)

    testtree.print_tree()


def test2():

    testtree = RBTree()
    for i in range(10):
        testtree.insert(i,i)

    testtree.print_tree()
    print(testtree.get_size())

    for i in range(11):
        testtree.remove(node=testtree.get_min())
        testtree.print_tree()


def test3():

    tree = RBTree()
    vals = []
    for i in range(10):
        vals.append(i)
    shuffle(vals)
    for i in range(10):
        tree.insert(vals[i])

if __name__ == '__main__':
    test2()