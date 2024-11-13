import Tree
from Tree import TreeNode

'''The functions generate_tree and generate_tree1 have the scope of generating the two trees the calculations
will be carried out on. To modify the structure of the trees, modify the code of these two functions.'''
def generate_tree():
    """
    Function to generate the first binary tree that represent a phylogenetic tree.
    :return: The root of the tree.
    """
    root = TreeNode("1")
    root.left = TreeNode("2")
    root.left.left = TreeNode("j")
    root.left.right = TreeNode("k")
    root.right = TreeNode("3")
    root.right.left = TreeNode("a")
    root.right.right = TreeNode("4")
    root.right.right.left = TreeNode("b")
    root.right.right.right = TreeNode("5")
    root.right.right.right.left = TreeNode("c")
    root.right.right.right.right = TreeNode("6")
    root.right.right.right.right.left = TreeNode("d")
    root.right.right.right.right.right = TreeNode("7")
    root.right.right.right.right.right.left = TreeNode("x")
    root.right.right.right.right.right.right = TreeNode("y")
    return root


def generate_tree1():
    """
    Function to generate the second binary tree that represent a phylogenetic tree.
    :return: The root of the tree.
    """

    root = TreeNode("1")
    root.left = TreeNode("2")
    root.left.left = TreeNode("j")
    root.left.right = TreeNode("k")
    root.right = TreeNode("3")
    root.right.left = TreeNode("a")
    root.right.right = TreeNode("4")
    root.right.right.left = TreeNode("b")
    root.right.right.right = TreeNode("5")
    root.right.right.right.left = TreeNode("x")
    root.right.right.right.right = TreeNode("6")
    root.right.right.right.right.left = TreeNode("c")
    root.right.right.right.right.right = TreeNode("7")
    root.right.right.right.right.right.left = TreeNode("d")
    root.right.right.right.right.right.right = TreeNode("y")
    return root


def find_lca(root, nodes):
    """
    Function that calculated the lowest common ancestor between the first element of the list nodes and the other elements.
    :param root: The root of the tree.
    :param nodes: The list of nodes we want to calculate the common LCA for.
    :return: The list ancestors, which contains all the lowest common ancestors.
    """
    ancestors = []
    for i in range(1, len(nodes)):
        ancestors.append(Tree.lowest_common_ancestors(root, nodes[0], nodes[i]))
    return ancestors


def find_paths_to_ancestors(ancestors, nodes, path):
    """
    Function that calculates the path from the nodes to their lowest commmon ancestors.
    :param ancestors: A list containing all the lowest common ancestors.
    :param nodes: A list containing the nodes.
    :param path: A List that will be filled with the path from a node to its lowest common ancestor.
    :return: A matrix containing all the paths.
    """
    paths = [[]]
    for i in range(len(ancestors)):
        Tree.hasPath(ancestors[i], path, nodes[i + 1])
        paths.append(path)
        path = []
    return paths


def find_path_to_ancestor_chosen_node(node, ancestors, paths):
    """
    Function that returns the path from the first node in the list nodes to the less deep ancestor.
    :param node: The first node in the list nodes.
    :param ancestors: All the lowest common ancestors.
    :param paths: The matrix containing all the paths.
    :return:
    """
    aux = []
    '''Calculate the path from the node to all the ancestors'''
    for ancestor in ancestors:
        path = []
        Tree.hasPath(ancestor, path, node)
        aux.append(path)

    '''Find the longest path and add it to the matrix paths.'''
    final_path = max(aux, key=len)
    index = aux.index(final_path)
    paths.insert(0, final_path)
    paths.remove([])
    return paths, ancestors[index]


def compute_embedding(paths):
    """
    Function that computes the embedding of a component in a tree.
    :param paths: The matrix of the paths from node to ancestor.
    :return: A dictionary that represents the embedding.
    """
    embedding = []
    seen_elements = {}
    for i in range(len(paths)):
        for j in range(len(paths[i]) - 1):

            '''for each element z in paths, check if it has already been encountered.'''
            if paths[i][j] not in seen_elements:
                '''If the z has not already been encountered, add a key in seen_element and set its associated
                list to be the following element in paths.'''
                seen_elements[paths[i][j]] = []
                seen_elements[paths[i][j]].append(paths[i][j+1])

            '''Check all the elements that follow z'''
            for k in range(i, len(paths)):
                start_index = j if k == i else 0
                for z in range(start_index, len(paths[k])):
                    if i == k and j == z:
                        continue
                    else:
                        '''If a new element w equal to z is found and the associated list of z is smaller than 2,
                        add the element that follows w to the associated list of z. z can not have more than 2 elements
                        in its associated list because the trees are binary.'''
                        if (paths[k][z] == paths[i][j]) and (len(seen_elements[paths[i][j]]) < 2) and (seen_elements[paths[i][j]][0] != paths[k][z + 1]):
                            seen_elements[paths[i][j]].append(paths[k][z + 1])

    return seen_elements


def remove_root(root, embedding):
    """
    Function that, given the embedding, removes the root node, since it is a 2-degree internal node with.
    :param root: The root to be removed.
    :param embedding: The embedding that needs to be adjusted.
    :return: The varible embedding, which now contains the embedding without the root.
    """

    '''After deleting the root, store its associated list into the variable values, which constists of two elements.
    Then loop through the embedding and, when an key x equal to one of the two elements in values if found, add the
    other element in the associated list of x.'''
    values = embedding[root]
    embedding.pop(root)

    for key, value in embedding.items():
        if key == values[0]:
            value.append(values[1])
            break
        if key == values[1]:
            value.append(values[0])
            break
    return embedding


def compute_reduced_embedding(root, embedding):
    """
    Function that removes useless elements from an embedding.
    :param root: The root of the tree.
    :param embedding: The emdedding to be reduced.
    :return:
    """
    local_embedding = {key: value[:] for key, value in embedding.items()}

    '''Find all the keys whose associated list consists of one element'''
    single_length_keys = [key for key, value in local_embedding.items() if len(value) == 1]

    '''Delete each single length key x and add their associated list to a key that has x in its associated list.'''
    for key in single_length_keys:
        value = local_embedding[key][0]
        local_embedding.pop(key)
        for k, v in local_embedding.items():
            updated_values = []
            for x in v:
                if x == key:
                    updated_values.append(value)
                else:
                    updated_values.append(x)

            local_embedding[k] = updated_values

    if len(local_embedding) > 1:
        local_embedding = remove_root(root, local_embedding)

    return local_embedding


def insert_new_label(index):
    """
    Function that keeps track of new labels to be added when needed.
    :param index: The index of the label to introduce next.
    :return: The label to introduce.
    """
    labels = ["k", "j", "w", "h", "i", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "z"]
    return labels[index]


def find_equal_cherries(embedding1, embedding2):
    """
    Function that, given two embeddings, finds if they share a common cherry.
    :param embedding1: The first embedding.
    :param embedding2: The second embedding.
    :return: The common cherry if it exists; otherwise, return False.
    """
    cherry = []

    '''Check the associated list of each key of the first embedding; if all the elements in it are not keys in the
    embedding, they form a cherry.'''
    for key, values in embedding1.items():
        if all(element not in embedding1 for element in values):
            cherry = values
            key1 = key
            break

    cherry = sorted(cherry, key=lambda x: x.val)

    '''Check the associated list of each key of the second embedding; if it is equal to the variable cherry, then
    it is a common cherry.'''
    for key, values in embedding2.items():
        values = sorted(values, key=lambda x: x.val)
        cherry_val = [obj.val for obj in cherry]
        values_val = [obj.val for obj in values]
        if cherry_val == values_val:
            key2 = key
            return (key1, key2)
    return False


def update_dictionary(embedding1, embedding2, index):
    """
    Function to delete common cherries.
    :param embedding1: The first embedding.
    :param embedding2: The second embedding.
    :param index: The index of the new label to insert.
    :return: The updated embeddings.
    """

    '''Store the common cherry into the variable result.'''
    result = find_equal_cherries(embedding1, embedding2)
    if result == False:
        return False

    '''Remove the cherry from the embeddings'''
    embedding1.pop(result[0])
    embedding2.pop(result[1])

    '''If, after deleting the common cherry the two embeddings are empty, they are topologically equivalent'''
    if len(embedding1) == 0 and len(embedding2) == 0:
        return True

    '''In both emdebbings, introduce a new label where the key of the cherry was deleted.'''
    for key, values in embedding1.items():
        if result[0] in values:
            for element in values:
                if element == result[0]:
                    element.val = insert_new_label(index)

    for key, values in embedding2.items():
        if result[1] in values:
            for element in values:
                if element == result[1]:
                    element.val = insert_new_label(index)
    return embedding1, embedding2


def same_restricted_embedding(embedding1, embedding2, index):
    """
    Function that iteratively deletes cherries to understand if two embeddings are topologically equivalent.
    :param embedding1: The firs embedding.
    :param embedding2: The second embedding.
    :param index: The index of the new label to introduce.
    :return: True if the embeddings are topologically equivalent, 0 otherwise.
    """

    '''Make a first call to update_dictionary to save the first result.'''
    result = update_dictionary(embedding1, embedding2, index)

    '''If the result is different from False and True, it contains the embeddings, therefore continue deleting cherries.
    If the result is True or False, return it.'''
    while result != False and result != True:
        result = update_dictionary(result[0], result[1], index + 1)
    return result


def check_shared_elements(embeddings_list, embedding):
    """
    Function that checks if a new embedding is not vertex disjoint with the previously calculated ones.
    :param embeddings_list: A list containing all the previously calculated embeddings.
    :param embedding: The embedding to check.
    :return: True if the embeddings are vertex disjoint, False otherwise.
    """
    for element in embeddings_list:
        for key in embedding:
            if key in element:
                return False
    return True


def check_split_chain(forest, chain):
    """
    Function that checks if a chain is split by some components
    :param forest: The forest where want to understand if the chain is split.
    :param chain: The chain to check.
    :return: True if the chain is split, false otherwise.
    """
    chain_set = set(chain)
    for component in forest:
        component_set = set(component)
        if chain_set.issubset(component_set):
            return False
    return True



def print_dictionary(dictionary):
    """
    Function to print a dictionary
    :param dictionary: The dictionary to be printed.
    :return:
    """
    for key, value in dictionary.items():
        if value is None:
            print(f"{key.val}: None")
        else:
            print(f"{key.val}: {[item.val for item in value]}")
