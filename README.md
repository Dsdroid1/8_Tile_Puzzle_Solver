# Assignment 1 (AI) : 8-tile puzzle solver

Assignment 1 for AI course, implementation of an 8-tile puzzle solver using bi-directional search

### Steps to execute

The program is written in python, to execute it, run
`python main.py`

The program will then ask for the initial config of the 8-tile puzzle.

#### Valid Inputs

We are using '0' to denote the empty space in the puzzle, and rest 1-8 as the other tiles.
Thus, the input should be treated as a flattened puzzle with values in range [0,8], each occuring exactly once.
`Sample Input: 1 0 2 3 4 5 6 7 8`
Once the config is supplied, we check if converting it to the goal state is possible or not using the parity test of inversions. If the solution is possible, the agent is called and it executes a bi-directional search to solve it in O(b^[d/2]) time and space. If the solution is not possible, we simply print that it is not possible and terminate. The bi-directional search uses BFS to search from both sides

#### Info about the solution:

- `Complete` - `Yes` (if solution exists, we will surely find it)
- `Optimal` - `Yes` (as the path-cost is equal to the depth)
- `Time Complexity` - `O(b^[d/2])` (as we explore from both sides, and hence require d/2 depth from each side)
- `Space Complexity` - `O(b^[d/2])`

#### Data Structures Used

- `Fringe list`(Containing yet to be explored nodes) - List data type of python, each element containing:
  - `config` : State representation of the 8-tile puzzle
  - `parent` : Parent node, that resulted in creation of this node
  - `action_from_parent` : Action to take from the parent state to reach this state
  - `depth` : The depth at which the config occurs, also equal to the path cost for this case.
- `Closed list`(Containing already expanded nodes from one direction) - Python dictionary (hashmap) with:
  - `key` : Numeric value of the state array
  - `value` : Node, containing all data mentioned in an element of a fringe list.

#### Output Format

The solution, if exists is printed with a step-by-step guide to reach the goal config
We print the details about each step, including :

- The depth of the step
- The config of the puzzle after performing the given step
- The step required to reach this config, from the just previous state
