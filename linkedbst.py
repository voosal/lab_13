"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log
import sys
import random
import time


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            stringg = ""
            if node != None:
                stringg += recurse(node.right, level + 1)
                stringg += "| " * level
                stringg += str(node.data) + "\n"
                stringg += recurse(node.left, level + 1)
            return stringg

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top == None:
                return 0
            else:
                return max(height1(i) for i in [top.left, top.right]) + 1

        return height1(self._root) - 1

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        if self.height() + 1 < 2 * log(2 * (len(list(self.inorder())) + 1)) - 1:
            return True
        else:
            return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        main_tree_list = list(self.inorder())

        while True:
            if high in main_tree_list or high == main_tree_list[0]:
                break
            high -= 1
        while True:
            if low in main_tree_list or low == main_tree_list[::-1]:
                break
            low += 1
        if low > high:
            return None

        high_spliter = main_tree_list.index(high) + 1
        low_spliter = main_tree_list.index(low)

        return main_tree_list[low_spliter:high_spliter]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        tree_list = list(self.inorder())
        self.clear()

        def rec_func(tree_list):
            divided_len = len(tree_list) // 2
            if not tree_list:
                return None
            else:
                return BSTNode(tree_list[divided_len], rec_func(tree_list[:divided_len]), \
                    rec_func(tree_list[divided_len + 1:]))

        self._root = rec_func(tree_list)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        tree_list = list(self.inorder())

        while item != tree_list[-1]:
            item += 1

            if item in tree_list:
                return tree_list[tree_list.index(item)]

        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        tree_list = list(self.inorder())

        while item != 0:
            item -= 1

            if item in tree_list:
                return tree_list[tree_list.index(item)]

        return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        tre = LinkedBST()
        sys.setrecursionlimit(100000)

        with open(path, 'r', encoding = 'utf-8') as file:
            list_file = list(i[:-1] for i in file)


        words_set = random.sample(list_file, 10000)
        start = time.time()
        for i in words_set:
            list_file.index(i)
        end = time.time()
        time_task_one = str(end - start)[:6]
        print(f'Time for the search using list: {time_task_one} seconds')

        difference = int(len(list_file) / 15000)
        half_list = list_file[:15000]
        words_set = random.sample(half_list, 10000)
        for word in half_list:
            tre.add(word)

        start = time.time()
        for word in words_set:
            tre.find(word)
        end = time.time()
        time_task_two = str((end - start) * difference)[:6]
        print("The next search is completed on a smaller amount of words (15000) as" + \
              "the bigger tree builds too long. The time is multiplied by the difference in length")
        print(f'Time for the search using alphabet tree: {time_task_two} seconds')

        tre.clear()

        words_set = random.sample(list_file, 10000)

        for item in random.sample(list_file, len(list_file)):
            tre.add(item)

        start = time.time()
        for word in words_set:
            tre.find(word)
        end = time.time()
        time_task_three = str((end - start))[:6]
        print(f'Time for the search using non alphabet tree: {time_task_three} seconds')


        tre.rebalance()

        start = time.time()
        for word in words_set:
            tre.find(word)
        end = time.time()
        time_task_four = str((end - start))[:6]
        print(f'Time for the search using balanced tree: {time_task_four} seconds')


tre = LinkedBST()
tre.demo_bst('words.txt')
