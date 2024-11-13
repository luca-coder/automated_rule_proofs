import Graph_operations
import Tree
import Operations
import time
from Tree import TreeNode

input = input("Enter 1 for chain reduction rule or 2 for interrupted chain theorem")

if input == "1":
    start_time = time.time()

    '''Variable that saves all the leaves of the two trees we want to calculate the distance for.'''
    '''To do: modify this list when generating new trees.'''
    all_leaves = ["a", "b", "c", "x", "y", "z"]

    '''Generation of the two trees.'''
    root1 = Graph_operations.generate_tree()
    root2 = Graph_operations.generate_tree1()

    Tree.print_inorder(root1)
    print(" ")
    Tree.print_inorder(root2)
    print(" ")

    '''Compute all the valid agreement forests and save them into the variable valid_forests.'''
    valid_forests = Operations.compute_valid_forests(root1, root2, all_leaves)

    '''Search all the forests to correct and save them into the variable forests_to_correct.'''
    forests_to_correct = Operations.find_forests_to_correct_chain(valid_forests)
    for forest in forests_to_correct:
        print(forest)
    print(" ")

    '''Modify all the forests and save the correction.'''
    corrected_forests = Operations.cut_and_rejoin_chain(forests_to_correct, root1, root2)
    for forest in corrected_forests:
        print(forest)
    print(" ")


    end_time = time.time()
    execution_time = end_time - start_time
    print(execution_time)

elif input == "2":
    start_time = time.time()
    leaves_set_to_check = {'x'}

    '''Variable that saves all the leaves of the two trees we want to calculate the distance for.'''
    '''To do: modify this list when generating new trees.'''
    all_leaves = ["x", "a", "b", "c", "d", "y", "j", "k"]

    '''Generation of the two trees.'''
    root1 = Graph_operations.generate_tree()
    root2 = Graph_operations.generate_tree1()

    Tree.print_inorder(root1)
    print(" ")
    Tree.print_inorder(root2)
    print(" ")

    '''Compute all the valid agreement forests and save them into the variable valid_forests.'''
    valid_forests = Operations.compute_valid_forests(root1, root2, all_leaves)

    '''Search all the forests to correct and save them into the variable forests_to_correct.'''
    forests_to_correct = Operations.find_forests_to_correct_interrupter(valid_forests, leaves_set_to_check)
    for forest in forests_to_correct:
        print(forest)
    print(" ")

    '''Modify all the forests and save the correction.'''
    corrected_forests = Operations.cut_and_rejoin_interrupter(forests_to_correct, root1, root2, leaves_set_to_check)
    for forest in corrected_forests:
        print(forest)

    end_time = time.time()
    execution_time = end_time - start_time
    print(execution_time)

else:
    print("Invalid input")
