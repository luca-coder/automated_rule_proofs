from itertools import combinations
import Graph_operations
import Tree
import Operations
from Tree import TreeNode
import copy


def partitions(set):
    """
    Function that calculates all the partitions of a set of elements by exploiting the library itertools,
    which is able to calculate all the combinations of a set.
    :param set: The set of leaveas of the trees.
    :return: By using the keyword yield, the function returns a partition and continues
    from where it left off the next time it is called.
    """
    if not set:
        yield []
        return
    for i in range(1, len(set)+1):
        for c in combinations(set[1:], i-1):
            first = [set[0]] + list(c)
            for rest in partitions([e for e in set if e not in first]):
                yield [first] + rest


def output_embedding(root, component):
    """
    Function that calculates the embedding of a component in the respective tree.
    :param root: The root of the tree.
    :param component: The subset of leaves we want to compute the embedding for.
    :return:
    """
    path = []
    paths = [[]]

    '''Search all the nodes with the labels contained into the variable component.'''
    nodes = Tree.find_nodes(root, component, [])

    '''Generate the embedding by employing the matrix paths.'''
    ancestors = Graph_operations.find_lca(root, nodes)
    paths = Graph_operations.find_paths_to_ancestors(ancestors, nodes, path)
    paths, ancestor = Graph_operations.find_path_to_ancestor_chosen_node(nodes[0], ancestors, paths)

    '''Create a dictionary to represent the embedding in a better way.'''
    embedding = Graph_operations.compute_embedding(paths)

    return embedding, ancestor


def check_forest_validity(forest, root1, root2):
    """
    Function to check if a forest, represented as a list of components, is valid.
    :param forest: The forest to check.
    :param root1: The first tree.
    :param root2: The second tree.
    :return: The parameter is_valid, which says if the forest is valid or not.
    """

    is_valid = True
    embeddings_list1 = []
    embeddings_list2 = []

    for component in forest:
        '''If one component of the forest has only one element, directly create the embedding dictionary by
        putting the respective node of the tree as key and None as associated value.'''
        if len(component) == 1:
            embedding1 = {Tree.find_nodes(root1, component, [])[0]: None}
            embedding2 = {Tree.find_nodes(root2, component, [])[0]: None}

            '''Check if the new embedding shares its only element with other embeddings. If yes, the respective 
            parameter result1 or result2 will be set to False.'''
            result1 = Graph_operations.check_shared_elements(embeddings_list1, embedding1)
            result2 = Graph_operations.check_shared_elements(embeddings_list2, embedding2)

            '''Employ two lists to save the embeddings. embeddings_list1 will contain all the embeddings that are 
            calculated on the first tree, while embeddings_list2 will contain all the embeddings that are calculated
            on the second tree.'''
            embeddings_list1.append(embedding1)
            embeddings_list2.append(embedding2)

            '''If result1 or result2 is False, the new embedding is not vertex disjoint with some previously
            calculated embeddings, therefore the forest is not valid.'''
            if result1 == False or result2 == False:
                is_valid = False
                break

        else:
            embedding1, ancestor1 = output_embedding(root1, component)
            embedding2, ancestor2 = output_embedding(root2, component)

            result1 = Graph_operations.check_shared_elements(embeddings_list1, embedding1)
            result2 = Graph_operations.check_shared_elements(embeddings_list2, embedding2)

            embeddings_list1.append(embedding1)
            embeddings_list2.append(embedding2)

            if result1 == True and result2 == True:
                '''Since the embedding has more than 1 element, calculate the restriction.'''
                reduced_embedding1 = Graph_operations.compute_reduced_embedding(ancestor1, embedding1)
                reduced_embedding2 = Graph_operations.compute_reduced_embedding(ancestor2, embedding2)

                '''Calculate if the restrictions are topologically equivalent or not; if they are not, 
                the forest is not valid.'''
                res = Graph_operations.same_restricted_embedding(copy.deepcopy(reduced_embedding1),
                                                                 copy.deepcopy(reduced_embedding2), 0)
                if res == False:
                    is_valid = False
            else:
                is_valid = False
                break
    return is_valid


def compute_valid_forests(root1, root2, all_leaves):
    """
    Function that calculates all the valid forests and returns them.
    :param root1: The first tree.
    :param root2: The second tree.
    :param all_leaves: The set of leaves of the trees.
    :return: The variable all_valid_forests, which stores all the valid forests.
    """
    all_valid_forests = []

    all_forests = list(Operations.partitions(all_leaves))
    for forest in all_forests:
        is_valid = check_forest_validity(forest, root1, root2)
        if is_valid == True:
            all_valid_forests.append(forest)
    return all_valid_forests


def find_forests_to_correct_chain(all_valid_forests):
    """
    Function that calculates the forests that need correction among all the valid ones with respect to the chain
    reduction rule.
    :param all_valid_forests: Variable that stores all the valid forests.
    :return: The variable forests_to_correct, which stores all the forests that need correction
    """
    forests_to_correct = []

    '''If a forest split the chain {a, b, c}, then it needs to be corrected and it is stored into forests_to_correct.'''
    for forest in all_valid_forests:
        if(Graph_operations.check_split_chain(forest, ['a', 'b', 'c']) == True):
            forests_to_correct.append(forest)
    return forests_to_correct


def compute_correction_chain(forest, root1, root2):
    """
    Function that corrects a forest with respect to the chain reduction rule.
    :param forest: The forest to correct.
    :param root1: The first tree.
    :param root2: The second tree.
    :return: The corrected forest.
    """
    components_to_modify = []
    safe_components = []
    leaves_list = []

    '''Each component that splits the chain is stored into the list components_to_modify; all the other components
    are stored into the list safe_components.'''
    for component in forest:
        if 'a' in component or 'b' in component or 'c' in component:
            components_to_modify.append(component)
        else:
            safe_components.append(component)
    safe_components_length = len(forest) - len(components_to_modify)

    '''Create the list all_forests where all the leaves of the components in components_to_modify are stored and 
    calculate all the partitions of this list.'''
    for component in components_to_modify:
        for element in component:
            leaves_list.append(element)
    all_forests = list(Operations.partitions(leaves_list))

    '''Join each partition of all_forests with safe_components and check if the result is a valid forest that does
    not split the chain and not larger than the initial forest to correct. If yes, return this forest, since it is 
    a proper correction.'''
    for corrected_forest in all_forests:
        if check_forest_validity(corrected_forest, root1, root2) == True and Graph_operations.check_split_chain(corrected_forest, ['a', 'b', 'c']) == False and len(corrected_forest) + safe_components_length <= len(forest):
            final_forest = [item for item in corrected_forest + safe_components if item != []]
            return final_forest


def cut_and_rejoin_chain(forests, root1, root2):
    """
    Function that calculates the correction for each forest with respect to the chain reduction rule.
    :param forests: List of all the forests that need to be corrected.
    :param root1: The first tree.
    :param root2: The second tree.
    :return: The variable corrected_forests, which stores all the corrections.
    """
    corrected_forests = []

    for forest in forests:
        corrected_forests.append(compute_correction_chain(forest, root1, root2))
    return corrected_forests


def find_forests_to_correct_interrupter(all_valid_forests, leaves_set_to_check):
    """
    Function that calculates the forests that need correction among all the valid ones with respect to the interrupted
    chain theorem.
    :param all_valid_forests: Variable that stores all the valid forests.
    :param leaves_set_to_check: Variable which indicated all the leaves contained into the set S'.
    :return:
    """
    forests_to_correct = []


    for forest in all_valid_forests:
        leaves_set_copy = leaves_set_to_check.copy()
        need_correction = False

        for component in forest:
            component_set = set(component)

            '''If a component consists of all the leaves contained into the set S', the forest does not need to be corrected, 
            since the interrupter is not used.
            If a component consists of a subset of the leaves contained into S', we can disregard these leaves, 
            because the interrupted is used by another component.
            If a component consists of leaves contained into S' as well as leaves that are not contained in S',
            that component uses the interrupter and therefore the forest needs to be corrected.
            '''
            if component_set == leaves_set_copy:
                need_correction = False
                break

            elif component_set.issubset(leaves_set_copy):
                leaves_set_copy -= component_set

            elif component_set & leaves_set_copy:
                if component_set != leaves_set_copy:
                    need_correction = True
                    break

        if need_correction:
            forests_to_correct.append(forest)

    return forests_to_correct


def compute_correction_interrupter(forest, root1, root2, leaves_set_to_check):
    """
    Function that corrects a forest with respect to the interrupted chain theorem.
    :param forest: The forest to correct.
    :param root1: The first tree.
    :param root2: The second tree.
    :param leaves_set_to_check: The leaves contained into the set S'.
    :return: The variable corrected_forests, which contains the correction.
    """
    new_leaves_set = []
    forests_to_check = []
    interrupter_component = [leaf for leaf in leaves_set_to_check]

    '''Create the list all_forests_not_interrupter that consists of all the partitions of the leaves not contained
    into S', and the list all_forests_interrupter that consists of all the partitions of the leaves contained
    into S.'''
    for component in forest:
        for leaf in component:
            new_leaves_set.append(leaf)
    new_leaves_set = [element for element in new_leaves_set if element not in leaves_set_to_check]
    all_forests_not_interrupter = list(Operations.partitions(new_leaves_set))
    all_forests_interrupter = list(Operations.partitions(interrupter_component))

    '''Join each partition in all_forests_not_interrupter and all_forests_interrupter to create an agreement forest,
    stored into the variable forests_to_check; in this way, we are sure that the interrupter is never used.'''
    for forest_interrupter in all_forests_interrupter:
        for forest_not_interrupter in all_forests_not_interrupter:
            forests_to_check.append(forest_interrupter + forest_not_interrupter)

    '''If forests_to_check is a valid agreement forest not larger than the initial one, then it is a proper
    correction and it is returned.'''
    for corrected_forest in forests_to_check:
        if check_forest_validity(corrected_forest, root1, root2) == True and len(corrected_forest) <= len(forest):
            return corrected_forest


def cut_and_rejoin_interrupter(forests, root1, root2, leaves_set_to_check):
    """
    Function that calculates the correction for each forest with respect to the interrupted chain theorem.
    :param forests: All the forests to be corrected.
    :param root1: The first tree.
    :param root2: The second tree.
    :param leaves_set_to_check: The leaves contained into S'.
    :return: The list corrected_forests, which contains all the corrections.
    """
    corrected_forests = []

    for forest in forests:
        corrected_forests.append(compute_correction_interrupter(forest, root1, root2, leaves_set_to_check))
    return corrected_forests
