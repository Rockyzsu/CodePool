#!/usr/bin/python3
"""
Given a tree, rearrange the tree in in-order so that the leftmost node in the
tree is now the root of the tree, and every node has no left child and only 1
right child.

Example 1:
Input: [5,3,6,2,4,null,8,1,null,null,null,7,9]

       5
      / \
    3    6
   / \    \
  2   4    8
 /        / \
1        7   9

Output: [1,null,2,null,3,null,4,null,5,null,6,null,7,null,8,null,9]

 1
  \
   2
    \
     3
      \
       4
        \
         5
          \
           6
            \
             7
              \
               8
                \
                 9
Note:

The number of nodes in the given tree will be between 1 and 100.
Each node will have a unique integer value from 0 to 1000.
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def __init__(self):
        self.prev = None
        self.root = None

    def increasingBST(self, root: TreeNode) -> TreeNode:
        """
        keep a previous index
        in-order is easy
        """
        self.dfs(root)
        return self.root

    def dfs(self, node):
        if not node:
            return

        self.dfs(node.left)
        if not self.prev:
            self.root = node
        else:
            self.prev.right = node
            node.left = None  # need test case to test it

        self.prev = node
        self.dfs(node.right)
