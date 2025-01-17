
def floats_are_equal(a, b, eps=1e-3):
    #Returns True if a and b are within eps of each other
    return abs(a - b) < eps

class Node:
    def __init__(self, data):
        self.data = data
        self.color = 'RED' # default color 
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:

    def __init__(self):
        self.NIL_LEAF = Node(None)  # Sentinel NIL leaf node
        self.NIL_LEAF.color = 'BLACK'
        self.NIL_LEAF.left = self.NIL_LEAF
        self.NIL_LEAF.right = self.NIL_LEAF
        self.root = self.NIL_LEAF
        self.size = 0
    def size(self):
        return self.size
    def _right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL_LEAF:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x
    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL_LEAF:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y


    def add(self, data):
        # print("add: " , data)
        self.size +=1
        node = Node(data)
        node.left = self.NIL_LEAF
        node.right = self.NIL_LEAF
        if self.root == self.NIL_LEAF:
            self.root = node
            node.color = 'BLACK'
        else:
            current = self.root
            while current != self.NIL_LEAF:
                parent = current
                if node.data < current.data:
                    current = current.left
                else:
                    current = current.right
            node.parent = parent
            if node.data < parent.data:
                parent.left = node
            else:
                parent.right = node
            self.insertFixup(node)

    def insertFixup(self, k):
        while k.parent and k.parent.color == 'RED':
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right
                if u.color == 'RED':
                    k.parent.color = 'BLACK'
                    u.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self._left_rotate(k)
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    self._right_rotate(k.parent.parent)
            else:
                u = k.parent.parent.left
                if u.color == 'RED':
                    k.parent.color = 'BLACK'
                    u.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self._right_rotate(k)
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    self._left_rotate(k.parent.parent)
        self.root.color = 'BLACK'

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def remove(self, data):
        # print("remove : ", data)
        node = self.root
        z = self.NIL_LEAF
        while node != self.NIL_LEAF:
            if node.data == data:
                z = node
            if node.data <= data:
                node = node.right
            else:
                node = node.left
            # if floats_are_equal(node.data , data): 
            #     z = node
            # if node.data <= data:
            #     node = node.right
            # else:
            #     node = node.left
        if z == self.NIL_LEAF:
            # print("Couldn't find key in the tree")
            return
        y = z
        y_original_color = y.color
        if z.left == self.NIL_LEAF:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL_LEAF:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 'BLACK':
            self.deleteFixup(x)
        self.size -=1
    def remove_str(self, data):
        # print("remove : ", data)
        node = self.root
        z = self.NIL_LEAF
        while node != self.NIL_LEAF:
            # if node.data == data:
            #     z = node
            # if node.data <= data:
            #     node = node.right
            # else:
            #     node = node.left
            if node.data == data: 
                z = node
            if node.data <= data:
                node = node.right
            else:
                node = node.left
        if z == self.NIL_LEAF:
            # print("Couldn't find key in the tree")
            return
        y = z
        y_original_color = y.color
        if z.left == self.NIL_LEAF:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL_LEAF:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 'BLACK':
            self.deleteFixup(x)
        self.size -=1
        
    def deleteFixup(self, x):
        while x != self.root and x.color == 'BLACK':
            if x == x.parent.left :
                s = x.parent.right
                if s.color == 'RED':
                    s.color = 'BLACK'
                    x.parent.color = 'RED'
                    self._left_rotate(x.parent)
                    s = x.parent.right
                if s.left.color == 'BLACK' and s.right.color == 'BLACK':
                
                    s.color = 'RED'
                    x = x.parent
                else:
                    if s.right.color == 'BLACK':
                        s.left.color = 'BLACK'
                        s.color = 'RED'
                        self._right_rotate(s)
                        s = x.parent.right
                    s.color = x.parent.color
                    x.parent.color = 'BLACK'
                    s.right.color = 'BLACK'
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 'RED':
                    s.color = 'BLACK'
                    x.parent.color = 'RED'
                    self._right_rotate(x.parent)
                    s = x.parent.left
                if s.left.color == 'BLACK' and s.right.color == 'BLACK':
                    s.color = 'RED'
                    x = x.parent
                else:
                    if s.left.color == 'BLACK':
                        s.right.color = 'BLACK'
                        s.color = 'RED'
                        self._left_rotate(s)
                        s = x.parent.left
                    s.color = x.parent.color
                    x.parent.color = 'BLACK'
                    s.left.color = 'BLACK'
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = 'BLACK'
    
    
    def popMinimum(self):
        if self.root == self.NIL_LEAF:
            return self.NIL_LEAF
        x = self.root
        while(x.left != self.NIL_LEAF):
            x = x.left
        value = x.data
        self.remove(x.data) # đã chinh sữa
        return value
    def popMinimum_str(self):
        if self.root == self.NIL_LEAF:
            return self.NIL_LEAF
        x = self.root
        while(x.left != self.NIL_LEAF):
            x = x.left
        value = x.data
        self.remove_str(x.data) # đã chinh sữa
        return value
    def popMaximum(self):
        if self.root == self.NIL_LEAF:
            return None
        x = self.root
        while x.right != self.NIL_LEAF:
            x = x.right
        value = x.data
        self.remove(x.data)
        return value
    def popMaximum_str(self):
        if self.root == self.NIL_LEAF:
            return None
        x = self.root
        while x.right != self.NIL_LEAF:
            x = x.right
        value = x.data
        self.remove_str(x.data)
        return value
    def _minimum(self, node):
        while node.left != self.NIL_LEAF:
            node = node.left
        return node
    def _maximum(self, node):
        while node.right != self.NIL_LEAF:
            node = node.right
        return node
    def minimum(self):
        if self.root == self.NIL_LEAF:
            return None
        return self._minimum(self.root).data
    def maximum(self):
        if self.root == self.NIL_LEAF:
            return None
        return self._maximum(self.root).data
    def search(self, data):
        current = self.root
        while current != self.NIL_LEAF and current.data != data:
            if data < current.data:
                current = current.left
            else:
                current = current.right
        return current if current != self.NIL_LEAF else None

