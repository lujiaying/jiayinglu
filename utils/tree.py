# coding: utf-8

"""树的相关函数"""


class TreeNode(object):
	"""
	Definition for a binary tree node
	"""
	def __init__(self, x):
		super(TreeNode, self).__init__()
		self.val = x
		self.left = None
		self.right = None

def constructTree(serialization):
	"""
	Construct a binary tree from the serialization.

	Args:
        serialization: serialization of the binary tree
	Returns:
	    root: root of the tree
	"""
	if not serialization:
		return None

	_stack = []
	root = TreeNode(serialization.pop(0))
	_stack.append(root)

	while _stack:
		if not serialization:
			break
		node = _stack.pop(0)
		n_left = serialization.pop(0)
		if n_left == '#':
			node.left = None
		else:
			node.left = TreeNode(n_left)
			_stack.append(node.left)
		n_right = serialization.pop(0)
		if n_right == '#':
			node.right = None
		else:
			node.right = TreeNode(n_right)
			_stack.append(node.right)

	return root


def levelOrderTraversal(root):
	"""
	Given a binary tree, return the level order traversal of its nodes' values.

	Args:
	    root: root of the tree
	Returns:
	    result: a list of lists of integers

	Usage:
	>>> root = constructTree(['3', '9', '20', '#', '#', '15', '7'])
	>>> levelOrderTraversal(root)
	[['3'], ['9', '20'], ['15', '7']]
	"""
	if not root:
	    return []
	
	current_level = 1
	_queue = [(root, current_level)]
	result = []
	level_result = []
	
	while _queue:
	    node, level = _queue.pop(0)
	    if node.left:
	        _queue.append((node.left, level+1))
	    if node.right:
	        _queue.append((node.right, level+1))
	    if node:
	        if level == current_level:
	            level_result.append(node.val)
	        else:
	            result.append(level_result)
	            level_result = [node.val]
	            current_level = level
	else:            
	    result.append(level_result)            
	return result


def _test():
	import doctest
	doctest.testmod()

if __name__ == '__main__':
    _test()