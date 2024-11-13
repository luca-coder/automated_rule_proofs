class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def print_inorder(node):
    if node:
        print_inorder(node.left)
        print(node.val, end=' ')
        print_inorder(node.right)


def find_nodes(root, component, nodes_list):
    """
    Function that, given a list of labels, search the respective nodes in the tree.
    :param root: The root of the tree.
    :param component: The list of labels in a component.
    :param nodes_list: An empty list that will store the nodes.
    :return: The variable nodes list.
    """
    if root:
        for element in component:
            if root.val == element:
                nodes_list.append(root)
        find_nodes(root.left, component, nodes_list)
        find_nodes(root.right, component, nodes_list)
        return nodes_list


def lowest_common_ancestors(root, p, q):
    """
    Function that calculates the lowest common ancestor between two nodes.
    :param root: The root of the tree.
    :param p: The first node.
    :param q: The second node.
    :return: The lowest common ancestor.
    """
    if root == None:
        return None

    if p == root or q == root:
        return root

    left_lca = lowest_common_ancestors(root.left, p, q)
    right_lca = lowest_common_ancestors(root.right, p, q)

    if left_lca and right_lca:
        return root

    return left_lca if left_lca else right_lca


def hasPath(root, arr, x):
    if (not root):
        return False

    arr.append(root)

    if (root == x):
        return True

    if (hasPath(root.left, arr, x) or
            hasPath(root.right, arr, x)):
        return True

    arr.pop(-1)
    return False


def printPath(root, x):
    arr = []
    if (hasPath(root, arr, x)):
        for i in range(len(arr) - 1):
            print(arr[i], end="->")
        print(arr[len(arr) - 1])

    else:
        print("No Path")