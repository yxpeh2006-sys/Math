import matplotlib.pyplot as plt
import networkx as nx

from setup import *
from graph import *

def main():

    input_n = input('Select number of moves n for Alice: ')
    try:
        n = int(input_n)
    except Exception():
        raise Exception('Input must be an integer.')
    
    graph = Graph()

    for _ in range(n):
        print('Current triangles in the format (label, area, neighbours_list):')
        graph.print()
        display_graph(load_graph(graph))

        input_node_label = input('Select triangle to split: ')

        try:
            node_label = int(input_node_label)
        except Exception():
            raise Exception('Input must be an integer.')
        
        if node_label >= graph.size or node_label < 0:
            raise Exception('Input must be a valid triangle label.')

        graph.nodes[node_label].print()
        input_split_areas = input('Select split areas: ')

        try:
            split_areas = [float(area) for area in input_split_areas.split()]
        except Exception():
            raise Exception('Input must contain exactly 3 space-separated numbers.')

        graph.split(node_label, split_areas)

    print('No more turns for Alice, now Bob chooses 3 neighbouring triangles.')

    while True:
        choice = input('View all current triangles? (y/n) ')
        if choice == 'y':
            graph.print()
            display_graph(load_graph(graph))
            break
        elif choice == 'n':
            break

    input('Enter any key to view the choices of Bob.')

    print('Bob chooses the following triangles:')
    graph.print_triangle_choice()

    while True:
        choice = input('View Hamiltonian cycle? (y/n) ')
        if choice == 'y':
            graph.print_simplified_path()
            display_path(graph)
            break
        elif choice == 'n':
            break


if __name__ == '__main__':
    main()