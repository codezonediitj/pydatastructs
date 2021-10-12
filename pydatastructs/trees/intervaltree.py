__all__ = [
    'Node',
    'IntervalTree'
]


class Node(object):
    """
    Abstract interval tree node.

    Parameters
    ==========

    interval
        Required, An interval which is represented
        as a pair in tuple (low, high).

    """
    def __init__(self, interval):
        self.interval = interval
        self.left_child = None
        self.right_child = None
        self.Max = None

    def hasChild(self):
        """
        Checks if Node has child or not.

        Returns
        =======

        True
            If the node has a left child or right child or both.

        False
            If the node does not has any child.

        """
        if self.left_child or self.right_child:
            return True
        return False

    def maxOfChild(self):
        """
        Returns interval with maximum high value in subtree
        rooted with this node

        Returns
        =======

        interval
            interval with maximum high value in subtree rooted with this node.
        """
        child_interval = list()
        if(self.left_child):
            child_interval.append(self.left_child.interval)
        if(self.right_child):
            child_interval.append(self.right_child.interval)
        return max(child_interval)


class IntervalTree(object):
    """
    Abstract binary tree.

    Parameters
    ==========

    key
        Required, root node of the tree.

    """
    def __init__(self, root):
        self.root = root

    def addNode(self, new_node):
        """
        Adds a new node to the tree.

        Parameters
        ==========

        Node
            Required, new node to be added in tree.

        Returns
        =======

        None

        """
        node = self.root
        while(node is not None):
            if(new_node.interval[0] <= node.interval[0]):
                if(node.left_child is None):
                    node.left_child = new_node
                    return
                node = node.left_child
            else:
                if(node.right_child is None):
                    node.right_child = new_node
                    return
                node = node.right_child

    def searchIntervalOverlap(self, query_node):
        """
        A utility function to search if any node overlaps with the given Node.

        Parameters
        ==========

        query_node
            Required, Node to be searched for overlapping.

        Returns
        =======

        Node, Node, boolean

        Node:
            parent_node
                Parent Node of the child node to be deleted.
            None
                if given interval node does not overlap with another node.

        Node:
            child_node
                Child node to be deleted.
            None
                if given interval node does not overlap with another node.

        boolean:
            True
                if given interval node overlaps with another node.
            False
                if given interval node does not overlap with another node

        """
        p_node = None
        c_node = self.root
        while(c_node):
            if(self.isOverlapping(c_node.interval, query_node)):
                # print("Overlapping with ", c_node.interval)
                return p_node, c_node, True
            else:
                p_node = c_node
                if(c_node.Max >= query_node[0]):
                    c_node = c_node.left_child
                else:
                    c_node = c_node.right_child
        return None, None, False

    def isOverlapping(self, interval_left, interval_right):
        """
        A utility function to check if given two nodes
        overlaps with each other.

        Parameters
        ==========

        interval_left
            Required, left node to be searched for overlapping.

        interval_right
            Required, right node to be searched for overlapping.


        Returns
        =======
        True
            if the two given nodes overlap with each other

        False
            if the two given nodes does not overlap with each other

        """
        if((interval_left[0] <= interval_right[1]) and
                (interval_right[0] <= interval_left[1])):
            return True

        return False

    def maxOfSubtree(self, root_node):
        """
        A utility function to set root_node.Max as the maximum
        high value in subtree rooted with this node

        Parameters
        ==========

        root_node
            Root Node of the subtree to be searched for maximum value

        Returns
        =======

        None
        """
        if((not root_node.Max) and (root_node.hasChild())):
            max_array = []
            if(root_node.left_child):
                self.maxOfSubtree(root_node.left_child)
                max_array.append(root_node.left_child.Max)
            if(root_node.right_child):
                self.maxOfSubtree(root_node.right_child)
                max_array.append(root_node.right_child.Max)
            max_array.append(root_node.interval[1])
            root_node.Max = max(max_array)
            return

        else:
            root_node.Max = root_node.interval[1]
            return

    def constructMax(self):
        """
        Sets root.Max as the maximum high value in whole tree.

        """
        node = self.root
        self.maxOfSubtree(node)

    def printTree(self):
        """
        A utility function to print the Interval Tree

        """
        node_list = [self.root]
        it_print = []
        while(len(node_list) != 0):
            current_node = node_list[0]
            node_list.pop(0)
            it_print.append((current_node.interval, current_node.Max))
            # print(current_node.interval, current_node.Max)
            if(current_node.left_child is not None):
                node_list.append(current_node.left_child)
            if(current_node.right_child is not None):
                node_list.append(current_node.right_child)
        return it_print

    def delete_node(self, node_):
        """
        Deletes a given node from the tree

        Parameters
        ==========

        Node
            Required, node to be deleted from the tree.

        Returns
        =======

        True
            if interval node is present in tree and overlaps with another node.

        False
            if interval node does not overlap with any node.

        """
        parent_node, node_to_delete, _ = self.searchIntervalOverlap(node_)

        # If no overlap
        if not node_to_delete:
            return False

        if node_to_delete.hasChild():
            if node_to_delete.left_child:
                if self.whichChild(parent_node, node_to_delete) == "left":
                    parent_node.left_child = node_to_delete.left_child
                else:
                    parent_node.right_child = node_to_delete.left_child
                self.reloadTree(node_to_delete.right_child)
            else:
                if self.whichChild(parent_node, node_to_delete) == "left":
                    parent_node.left_child = node_to_delete.right_child
                else:
                    parent_node.right_child = node_to_delete.right_child
        else:
            if parent_node.left_child == node_to_delete:
                parent_node.left_child = None
            if parent_node.right_child == node_to_delete:
                parent_node.right_child = None
            return True

    def whichChild(self, p_node, c_node):
        """
        A utility function to check whether the given child node is
        left child or right child of the given parent node.

        Parameters
        ==========

        p_node
            Required, parent node.

        c_node
            Required, child node.

        Returns
        =======

        "left"
            if child node is left child of parent node.

        "right"
            if child node is right child of parent node.

        """
        if p_node.left_child == c_node:
            return "left"
        if p_node.right_child == c_node:
            return "right"

    def reloadTree(self, node_):
        if node_.hasChild():
            if node_.left_child:
                reloadTree(node_.left_child)
            if node_.right_child:
                reloadTree(node_.left_child)
        else:
            self.addNode(node_)
