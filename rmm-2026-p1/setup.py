import math

TRIANGLE_SIZE = 1.0     # Area of Alice's starting triangle

class Node():

    def __init__(self, label, area, neighbours):
        '''
        A node object represents a small triangle and has a label, an area, as well as
        a list of 3 neighbour nodes.

        Subsequently, to find Bob's strategy, we need to find a Hamiltonian cycle in
        the graph of triangles, so a node object also keeps track of its previous and
        next node in the Hamiltonian cycle.
        '''
        self.label = label
        self.area = area
        self.neighbours = neighbours
        self.path_prev = None
        self.path_next = None

    def represent(self):
        '''
        Represents a node object by a 3-tuple of the form (label, area, neighbour_labels).
        '''
        neighbour_labels = [neighbour.label if neighbour is not None else None 
                            for neighbour in self.neighbours]
        representation = (self.label, self.area, neighbour_labels)
        return representation

    def print(self):
        '''
        Prints the representation of the node object.
        '''
        print(self.represent())


class Graph():

    def __init__(self):
        '''
        A graph object has a dictionary of nodes in the format {label : node}, and
        also keeps track of its size, or number of nodes.

        Since Alice starts the game with 1 big triangle, the constructor makes 1 node.
        '''
        node = Node(0, TRIANGLE_SIZE, [None, None, None])
        self.nodes = {0: node}
        self.size = 1

    def print(self):
        '''
        Prints the nodes in the graph.
        '''
        for node in self.nodes.values():
            node.print()

    def split(self, node_label, split):
        '''
        Given the label of the triangle to split into three smaller triangles, and the
        areas of the 3 splits, modify the graph to represent the resultant triangulation.
        '''
        node = self.nodes[node_label]

        if len(split) != 3:
            raise Exception('Split is not of size 3.')

        split_sum = split[0] + split[1] + split[2]
        if not math.isclose(split_sum, node.area):
            raise Exception(f'split areas sum to {split_sum} which is not the original area {node.area}.')

        # We let node become one of the three split triangles, and we will create
        # two new nodes later.
        neighbour_1 = node.neighbours[1]
        if neighbour_1 is not None:
            neighbour_1.neighbours.remove(node)     # reset the neighbour relationship
        neighbour_2 = node.neighbours[2]
        if neighbour_2 is not None:
            neighbour_2.neighbours.remove(node)     # reset the neighbour relationship
        node.area = split[0]
        node.neighbours[1] = None       # reset the neighbour relationship
        node.neighbours[2] = None       # reset the neighbour relationship

        new_node_1 = Node(self.size, split[1], [node, neighbour_1, None])
        if neighbour_1 is not None:
            neighbour_1.neighbours.append(new_node_1)
        node.neighbours[1] = new_node_1     # make a new node and add in neighbour relationships
        self.nodes[self.size] = new_node_1  # add new node to the graph
        self.size += 1                      # update graph size

        new_node_2 = Node(self.size, split[2], [node, new_node_1, neighbour_2])
        if neighbour_2 is not None:
            neighbour_2.neighbours.append(new_node_2)
        node.neighbours[2] = new_node_2
        new_node_1.neighbours[2] = new_node_2   # make the second new node and add in neighbours
        self.nodes[self.size] = new_node_2      # add new node to the graph
        self.size += 1                          # update graph size

        # Inductively modify the Hamiltonian cycle after each split
        if self.size == 3:  # Base case: 0 -> 1 -> 2 -> 0
            self.nodes[0].path_prev = self.nodes[2]
            self.nodes[0].path_next = self.nodes[1]
            self.nodes[1].path_prev = self.nodes[0]
            self.nodes[1].path_next = self.nodes[2]
            self.nodes[2].path_prev = self.nodes[1]
            self.nodes[2].path_next = self.nodes[0]

        else:   # Inductive step
            path_prev = node.path_prev      # T0
            path_next = node.path_next      # T4

            # Expand the Hamiltonian cycle
            for candidate in [node, new_node_1, new_node_2]:
                if path_prev in candidate.neighbours:
                    first = candidate
                elif path_next in candidate.neighbours:
                    third = candidate
                else:
                    second = candidate
            
            path_prev.path_next = first
            first.path_prev = path_prev
            first.path_next = second
            second.path_prev = first
            second.path_next = third
            third.path_prev = second
            third.path_next = path_next
            path_next.path_prev = third

    def path(self):
        '''
        Returns a list of labels in the Hamiltonian cycle, returning back to
        the starting node and then the next node, so that we can check all possible
        consecutive triples by applying a sliding window along this list.
        '''
        current = self.nodes[0]
        labels = []
        for _ in range(self.size + 2):
            labels.append(current.label)
            current = current.path_next
        return labels

    def print_path(self):
        '''
        Prints the tuple representations of the nodes in the order of the
        Hamiltonian cycle, returning back to the start node.
        '''
        path = self.path()
        for label in path[:-1]:
            self.nodes[label].print()

    def print_simplified_path(self):
        '''
        Prints the list of node labels in the order of the Hamiltonian cycle,
        returning back to the start node.
        '''
        print(self.path()[:-1])

    def triangle_choice(self):
        '''
        Chooses 3 adjacent nodes in the Hamiltonian cycle which have a total area greater
        than 3 times the average triangle area.
        '''
        threshold = 3 * TRIANGLE_SIZE / self.size
        max_index = 0
        current_index = 0
        path_labels = self.path()
        for _ in range(self.size):
            if sum(self.nodes[path_labels[current_index + i]].area for i in range(3)) >= threshold:
                return (self.nodes[path_labels[current_index + i]] for i in range(3))
            current_index += 1        

    def print_triangle_choice(self):
        '''
        Prints the representations of the 3 chosen nodes, and their total area.
        '''
        triangle_choice = self.triangle_choice()
        total_area = 0
        for triangle in triangle_choice:
            triangle.print()
            total_area += triangle.area
        print(f'Sum of areas: {total_area:.1f}')