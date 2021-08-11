"""
Assignment 1 for Course AI(W21) by BT18CSE046 
This program will be used to detetrmine the solution for a given instance of the 8-tile puzzle,
using an uninformed search technique namely Bi-directional search.
"""
# Import required libraries
import sys
import math

# Function to determine whether the given instance of the 8-tile puzzle is solvable or not.
def check_solvable(instance, goal_state):
    # We are using '0' in the array to denote empty space, it will not be counted towards the inversions
    # Check the no.of inversions in instance as well as the goal state
    inversions_instance = 0
    inversions_goal = 0
    for i in range(0, len(instance)-1):
        for j in range(i+1, len(instance)):
            if instance[i] != 0 and instance[j] != 0 and instance[j] < instance[i]:
                inversions_instance += 1
            if goal_state[i] != 0 and goal_state[j] != 0 and goal_state[j]< goal_state[i]:
                goal_state += 1
    solvable = False
    # The parity of inversions of instance and goal must be same
    if inversions_instance % 2 == inversions_goal % 2:
        solvable = True
    return solvable

# Helper function to visualize the state of the 8 tile puzzle
def visualize_state(current_state):
    for i in range(0, len(current_state)):
        if i % 3 == 0 and i != 0:
            print("")
        print(current_state[i], end=" ")
    print("")

# Helper function to return a unique numeric value associated with every possible config
def numeric_of_state(current_config):
    # This function will help in generating a unique numeric key associated with each state, for storing in a hash map
    value = 0
    place_value = 1 
    for i in reversed(range(0, len(current_config))):
        value += current_config[i]*place_value
        place_value *= 10
    return value

# Defines the successor function for the agent, returns the possible configurations the next move can lead to
def successor_function(current_config):
    # The allowed motion for the empty tile is up,down,right,left and that too only if the space is available(not on boundary)
    # Get the position of the tile in a 3x3 arrangement
    position = current_config.index(0)
    states = []
    if position < 0:
        print('Error occured!')
        sys.exit()
    else:
        i = math.floor(position/3)
        j = position % 3
        
        # Try to move tile in upward direction
        if i-1 >= 0:
            tmp_list = current_config.copy()
            tmp_list[position] = tmp_list[(i-1)*3+j]
            tmp_list[(i-1)*3+j] = 0
            states.append({"new_state":tmp_list,"move":"up"})
        # Try to move tile in downward direction 
        if i+1 <= 2:
            tmp_list = current_config.copy()
            tmp_list[position] = tmp_list[(i+1)*3+j]
            tmp_list[(i+1)*3+j] = 0
            states.append({"new_state":tmp_list,"move":"down"})
        # Try to move tile in left direction
        if j-1 >= 0:
            tmp_list = current_config.copy()
            tmp_list[position] = tmp_list[i*3+(j-1)]
            tmp_list[i*3+(j-1)] = 0
            states.append({"new_state":tmp_list,"move":"left"})
        # Try to move tile in right direction
        if j+1 <= 2:
            tmp_list = current_config.copy()
            tmp_list[position] = tmp_list[i*3+(j+1)]
            tmp_list[i*3+(j+1)] = 0
            states.append({"new_state":tmp_list,"move":"right"})
    return states

# The bi-directional searching function for the bi-directional search
def bidirectional_search(forward_fringe_list, backward_fringe_list, closed_list):
    # The closed list is populated by only 1 direction of the search
    # We assume that we are storing those states that are expanded from the forward direction
    found = False
    while not found:
        if len(forward_fringe_list) != 0:
            # Do BFS
            current_forward_state =  forward_fringe_list[0]
            current_depth = current_forward_state['depth']
            # Get all other nodes at the same depth for BFS
            while len(forward_fringe_list) != 0 and forward_fringe_list[0]['depth'] == current_depth:
                current_forward_state =  forward_fringe_list.pop(0) 
                # Remember this state as visited
                if closed_list.get(numeric_of_state(current_forward_state['config'])) is None:
                    closed_list[numeric_of_state(current_forward_state['config'])] = current_forward_state
                    # Add all its successors to the fringe list for expansion
                    states = successor_function(current_forward_state['config'])
                    for state in states:
                        forward_fringe_list.append({'config': state['new_state'],'parent': current_forward_state,'depth':current_forward_state['depth']+1,'action_from_parent':state['move']})
            
        
        if len(backward_fringe_list) != 0:
            current_backward_state = backward_fringe_list[0]
            current_backward_depth = current_backward_state['depth']
            while not found and len(backward_fringe_list) != 0 and backward_fringe_list[0]['depth'] == current_backward_depth:
                current_backward_state = backward_fringe_list.pop(0)
                # Check if this state was already visited by the forward search
                if closed_list.get(numeric_of_state(current_backward_state['config'])) is not None:
                    # Solution has been found
                    found = True
                    # Get the same node generated from the forward direction
                    intersection_node = closed_list.get(numeric_of_state(current_backward_state['config']))
                else:
                    # Consider this state for expansion on reverse direction
                    states = successor_function(current_backward_state['config'])
                    for state in states:
                        backward_fringe_list.append({'config': state['new_state'],'parent': current_backward_state,'depth':current_backward_state['depth']+1,'action_from_parent':state['move']})
    # Trace the solution using the intersection node
    depth = 0
    initial_to_intersection_path = []
    intersection_to_goal_path = []
    path_tracing_node = intersection_node
    # Trace the path from the initial state to the intersection node
    while path_tracing_node is not None:
        initial_to_intersection_path.append(path_tracing_node)
        path_tracing_node = path_tracing_node['parent']
        depth += 1
    initial_to_intersection_path.reverse()

    # Now, create the path from intersection to goal, and also invert the parent direction from backward to forward
    reverse_path_tracing_node = current_backward_state['parent']
    # Contains the parent according to the forward direction, for the backward search list
    previous_node = current_backward_state
    previous_node.update({'parent':initial_to_intersection_path[-1]})
    # Stores the action required to move in backward direction from node to parent, and hence will be inverted to get the movement in forward direction
    action_from_parent = current_backward_state['action_from_parent']
    while reverse_path_tracing_node is not None:
        # Invert the stats
        reverse_path_tracing_node.update({'depth':depth})
        parent_node_in_reverse_direction = reverse_path_tracing_node['parent']
        # Update parent to normalize the result in single direction
        reverse_path_tracing_node.update({'parent':previous_node})
        previous_node = reverse_path_tracing_node
        next_node_reversed_action = reverse_path_tracing_node['action_from_parent'] 
        # Update the move for forward direction
        if action_from_parent == 'up':
            reverse_path_tracing_node.update({'action_from_parent':'down'})
        elif action_from_parent == 'down':
            reverse_path_tracing_node.update({'action_from_parent':'up'})
        elif action_from_parent == 'left':
            reverse_path_tracing_node.update({'action_from_parent':'right'})
        elif action_from_parent == 'right':
            reverse_path_tracing_node.update({'action_from_parent':'left'})
        action_from_parent = next_node_reversed_action
        intersection_to_goal_path.append(reverse_path_tracing_node)
        reverse_path_tracing_node = parent_node_in_reverse_direction
        depth += 1
    # Combine the 2 lists
    initial_to_intersection_path.extend(intersection_to_goal_path)
    solution_states = initial_to_intersection_path
    # Return the solution states
    return solution_states

# The code for the problem-solving/search-based agent using bi-directional search
def agent(goal_config, instance):
    # For each state, we will store config, parent, depth(here it is equal to cost) and action taken from parent state
    initial_state = {'config': instance, 'parent': None, 'depth': 0, "action_from_parent": None}
    # Searching from both direction
    goal_state = {'config': goal_config, 'parent': None, 'depth': 0, "action_from_parent": None}
    # Both fringe lists are sorted by the depth from the respective initial configs
    forward_fringe_list = [initial_state]
    backward_fringe_list = [goal_state]
    # The closed list will be a hashmap of states, where the key will be the numeric value of the state config
    closed_list = {}
    solution = bidirectional_search(forward_fringe_list, backward_fringe_list, closed_list)
    # Print the solution
    print(f'No.of moves required:{len(solution)-1}')
    for state in solution:
        print(f'Depth: {state["depth"]}')
        print('Current state:')
        visualize_state(state['config']) 
        print(f'Action required from previous state:{state["action_from_parent"]}')

# The driver code that runs the program
if __name__ == "__main__":
    # The desired goal state, flattened as a list
    goal_config = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    # The input state for the 8-tile puzzle
    # Example of input : Solvable-0 8 2 1 4 3 7 6 5, Unsolvable- 8 1 2 0 4 3 7 6 5
    # Simple solvable input - 1 0 2 3 4 5 6 7 8
    instance = input('Enter the flattened config of the 8-tile puzzle with numbers from 1-8(separated by spaces) and 0 for the empty tile:')
    instance = list(map(int,instance.strip().split(" ")))

    # Check whether the given instance is solvable
    # If it is solvable, call the agent routine to solve it
    solvable = check_solvable(instance, goal_config)
    if solvable:
        print('This instance can be solved')
        agent(goal_config, instance)
    else:
        print('Error! The given instance is not solvable and the program will terminate')
