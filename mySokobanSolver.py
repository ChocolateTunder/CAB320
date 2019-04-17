
'''

    2019 CAB320 Sokoban assignment

The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

You are not allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the 
interface and triggers to a fail for the test of your code.
 
# by default does not allow push of boxes on taboo cells
SokobanPuzzle.allow_taboo_push = False 

# use elementary actions if self.macro == False
SokobanPuzzle.macro = False 

'''

# you have to use the 'search.py' file provided
# as your code will be tested with this specific file
import search

import sokoban



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (9683836, 'Rafael', 'Alves'), (9935100, 'Sophie', 'Rogers') ]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
   
#This class represents a directed graph  
# using adjacency list representation 
class Graph: 
    
    paths = []
    
    def __init__(self,vertices): 
        #No. of vertices 
        self.V= vertices  
          
        # default dictionary to store graph 
        self.graph = defaultdict(list)  
   
    # function to add an edge to graph 
    def addEdge(self,u,v): 
        self.graph[u].append(v) 
   
    '''A recursive function to print all paths from 'u' to 'd'. 
    visited[] keeps track of vertices in current path. 
    path[] stores actual vertices and path_index is current 
    index in path[]'''
    def printAllPathsUtil(self, u, d, visited, path): 
  
        # Mark the current node as visited and store in path 
        visited.append(u)
        path.append(u) 
        
        # If current vertex is same as destination, then print 
        # current path[] 
        if u == d: 
            self.paths.append(path)
        else: 
            # If current vertex is not destination 
            #Recur for all the vertices adjacent to this vertex 
            for i in self.graph[u]: 
                if visited[i]==False: 
                    self.printAllPathsUtil(i, d, visited, path) 
                      
        # Remove current vertex from path[] and mark it as unvisited 
        path.pop() 
        visited.remove(u)
        
   
   
    # Prints all paths from 's' to 'd' 
    def printAllPaths(self,s, d): 
  
        # Mark all the vertices as not visited 
        visited =[False]*(self.V) 
  
        # Create an array to store paths 
        path = [] 
  
        # Call the recursive helper function to print all paths 
        self.printAllPathsUtil(s, d,visited, path) 
   


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A cell inside a warehouse is 
    called 'taboo' if whenever a box get pushed on such a cell then the puzzle 
    becomes unsolvable.  
    When determining the taboo cells, you must ignore all the existing boxes, 
    simply consider the walls and the target cells.  
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner inside the warehouse and not a target, 
             then it is a taboo cell.
     Rule 2: all the cells between two corners inside the warehouse along a 
             wall are taboo if none of these cells is a target.
    
    @param warehouse: a Warehouse object

    @return
       A string representing the puzzle with only the wall cells marked with 
       an '#' and the taboo cells marked with an 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    X,Y = zip(*warehouse.walls)
    x_size, y_size = 1+max(X), 1+max(Y)
    vis = [[" "] * x_size for y in range(y_size)]
    for (x,y) in warehouse.walls:
        vis[y][x] = "#"
    for (x,y) in warehouse.targets:
        vis[y][x] = "."
    vis[warehouse.worker[1]][warehouse.worker[0]] = " "
    for (x,y) in warehouse.boxes:
            if vis[y][x] == ".": # if on target
                vis[y][x] = "."
            else:
                vis[y][x] = " "
            
    "Begin taboo code"
    row = []
    column = []
    started = False
    inside = [[False] * x_size for y in range(y_size)]
    i = 0
    
    "Creates a list with coordinates of empty squares"
    for line in vis:
        j = 0
        for place in line:
            if place == " " and j > 0 and i > 0 and j < max(X) and i < max(Y):
                column.append(j)
                row.append(i)
            j += 1
        i += 1
        
    "Checks if squares are within warehouse walls"
    "2 run throughs seems to tag everything"
    for i in range(0,2):
        for x in range(max(X)):
            for y in range(max(Y)):
                "Tag first top left corner as inside"
                if (vis[y-1][x] == "#" and vis[y][x-1] == "#" and \
                started == False):
                    started = True
                    inside[y][x] = True
                "Targets are assumed to be inside"
                if vis[y][x] == ".":
                    inside[y][x] = True
                "Check if surroundings are inside"
                if vis[y][x] != "#":
                    if(inside[y-1][x] == True or \
                       inside[y][x-1] == True or \
                       inside[y+1][x] == True or \
                       inside[y][x+1] == True or inside[y-1][x-1] == True or \
                       inside[y-1][x+1] == True or inside[y+1][x-1] == True or \
                       inside[y+1][x+1] == True):
                        inside[y][x] = True
        i += 1
        
    for i in row:
        for j in column:
            if vis[i][j] == " ": 
                "Check if space is a corner"
                if (vis[i-1][j] == "#" or vis[i+1][j] == "#") and \
                    (vis[i][j-1] == "#" or vis[i][j+1] == "#") and \
                     inside[i][j] == True:
                     vis[i][j] = "X"
                "Check if at end of tunnel"
                if (((vis[i-1][j] == "#" and vis[i+1][j] == "#") and \
                     (vis[i][j-1] == "#" or vis[i][j+1] == "#")) or \
                   ((vis[i][j-1] == "#" and vis[i][j+1] == "#")) and \
                    (vis[i+1][j] == "#" or vis[i-1][j] == "#") and \
                     inside[i][j] == True):
                     vis[i][j] = "X"
                     
    "Have to blank out targets in other loop or it doesn't work"                 
    for i in row:
        for j in column:
            if vis[i][j] == ".":
                vis[i][j] = " "    
    """
    'Test to see if all cells are tagged as inside'                
    for i in row:
        for j in column:
            if inside[i][j] == True:    
                vis[i][j] = "O"
    """
    
    """use vis = "\n".join(["".join(line) for line in vis]) and print vis"""
    "To get rid of literal /n in string"            
    return "\n".join(["".join(line) for line in vis])
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    Each instance should have at least the following attributes
    - self.allow_taboo_push
    - self.macro
    
    When self.allow_taboo_push is set to True, the 'actions' function should 
    return all possible legal moves including those that move a box on a taboo 
    cell. If self.allow_taboo_push is set to False, those moves should not be
    included in the returned list of actions.
    
    If self.macro is set True, the 'actions' function should return 
    macro actions. If self.macro is set False, the 'actions' function should 
    return elementary actions.
    
    
    '''
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' function is needed
    #     to satisfy the interface of 'search.Problem'.

    allow_taboo_push = True 
    
    macro = False
    
    def __init__(self, warehouse):
        self.allow_taboo_push = False
        self.macro = False
        self.initial = warehouse.__str__()
        self.goal = self.createGoalState(warehouse)
        
    def createGoalState(self, warehouse):
        X,Y = zip(*warehouse.walls)
        x_size, y_size = 1+max(X), 1+max(Y)
        vis = [[" "] * x_size for y in range(y_size)]
        for (x,y) in warehouse.walls:
            vis[y][x] = "#"
        for (x,y) in warehouse.targets:
            vis[y][x] = "$"
        vis[warehouse.worker[1]][warehouse.worker[0]] = " "
        for (x,y) in warehouse.boxes:
            vis[y][x] = " "

        row = []
        column = []
        i = 0
        for line in vis:
            j = 0
            for place in line:
                if place == " " and j > 0 and i > 0 and j < max(X) and i < max(Y):
                    column.append(j)
                    row.append(i)
                j += 1
            i += 1     
            
        return "\n".join(["".join(line) for line in vis])
    
    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        
        taboo_map = taboo_cells(state)
        # Get list of taboo cell locations
        taboo = list(sokoban.find_2D_iterator(taboo_map, "X")) # taboo cell
        
        # Get list of box locations
        boxes = state.boxes
        
        # Get location of worker
        worker = state.worker
        
        # Get locations of walls
        walls = state.walls
        
        nexto_boxes = []
        abv_bel_boxes = []
        
        actions = []
        no_up = False
        no_down = False
        no_left = False
        no_right = False
        
    
        # Test for adjacent boxes
        for i in range(0, len(boxes)):
            # Test box next to worker
            if abs(boxes[i][0] - worker[0]) == 1:
                nexto_boxes.append(boxes[i])
            # Test box above or below worker
            elif abs(boxes[i][1] - worker[1]) == 1:
                abv_bel_boxes.append(boxes[i])
        

        # Test if any boxes above or below
        if abv_bel_boxes:
            for i in range(0, len(abv_bel_boxes)):
                # Box above
                if (abv_bel_boxes[i][1] < worker[1]):
                    # Test taboo cell above box
                    for j in range(0 , len(taboo)):
                        # find correct x coordinate and test if directly above
                        if abv_bel_boxes[i][0] == taboo[j][0] and abv_bel_boxes[i][1] - 1 == taboo[j][1]:
                            # Test internal variable
                            if self.allow_taboo_push == False:
                                no_up = True
                            else:
                                no_up = False
                    # test wall directly above box
                    for j in range(0, len(walls)):
                        # Test wall directly above box
                        if abv_bel_boxes[i][1] - 1 == walls[j][1] and abv_bel_boxes[i][0] == walls[j][0]:
                            no_up = True
                            
                    # Test if another box above current box
                    for j in range(0, len(boxes)):
                        if abv_bel_boxes[i][1] - 1 == boxes[j][1] and abv_bel_boxes[i][0] == boxes[j][0]:
                            no_up = True
                            
                        
                # Test box below worker
                elif abv_bel_boxes[i][1] > worker[1]:
                    for j in range(0 , len(taboo)):
                        # find correct x coordinate and test if directly below
                        if abv_bel_boxes[i][0] == taboo[j][0] and abv_bel_boxes[i][1] + 1 == taboo[j][1]:
                            # Test internal variable
                            if self.allow_taboo_push == False:
                                no_down = True
                            else:
                                no_down = False
                    # Test if box directly above wall
                    for j in range(0, len(walls)):
                        if abv_bel_boxes[i][1] + 1 == walls[j][1] and abv_bel_boxes[i][0] == walls[j][0]:
                            no_down = True
                    # Test if box directly above another box
                    for j in range(0, len(boxes)):
                        if abv_bel_boxes[i][1] + 1 == boxes[j][1] and abv_bel_boxes[i][0] ==  boxes[j][0]:
                            no_down = True
                    
                    
                
        # If there are any adjacent boxes
        if nexto_boxes:
            for i in range(0, len(nexto_boxes)):
                # Test box to the left of worker
                if (nexto_boxes[i][0] < worker[0]):
                    # Test taboo cell to the left of box
                    for j in range(0, len(taboo)):
                        # Find correct y coordinate and test if directly to the left of box
                        if nexto_boxes[i][1] == taboo[j][1] and nexto_boxes[i][0] - 1 == taboo[j][0]:
                            # Test internal taboo variable
                            if self.allow_taboo_push == False:
                                no_left = True
                            else:
                                no_left = False
                    # Test if wall directly to left of box
                    for j in range(0, len(walls)):
                        if nexto_boxes[i][0] - 1 == walls[j][0] and nexto_boxes[i][1] == walls[j][1]:
                            no_right = True 
                    # Test if another box directly to left of box
                    for j in range(0, len(boxes)):
                        if nexto_boxes[i][0] - 1 == boxes[j][0] and nexto_boxes[i][1] == boxes[j][1]:
                            no_right = True
                            
                # Test box to the right of worker
                elif nexto_boxes[i][0] > worker[0]:
                    # Test taboo cell to the right of the box
                    for j in range(0, len(taboo)):
                        # Find correct y coordinate and test if directly to the right of box
                        if nexto_boxes[i][1] == taboo[j][1] and nexto_boxes[i][0] + 1 == taboo[j][0]:
                            # test internal taboo variable
                            if self.allow_taboo_push == False:
                                no_right = True
                            else:
                                no_right = False
                    # Test if wall directly to right of box
                    for j in range(0, len(walls)):
                        if nexto_boxes[i][0] + 1 == walls[j][0] and nexto_boxes[i][1] == walls[j][1]:
                            no_down = True
                    # Test if another box directly to the right of the box
                    for j in range(0, len(walls)):
                        if nexto_boxes[i][0] + 1 == boxes[j][0] and nexto_boxes[i][1] == boxes[j][1]:
                            no_down = True
        
        # Test worker next to wall
        for i in range(0, len(walls)):
            # test if worker to the left of a wall
            if worker[0] - 1 == walls[i][0] and worker[1] == walls[i][1]:
                no_right = True
            # Test worker to the right of a wall
            if worker[0] + 1 == walls[i][0] and worker[1] == walls[i][1]:
                no_left = True
            # Test if worker below wall
            if worker[1] - 1 == walls[i][1] and worker[0] == walls[i][0]:
                no_up = True
            # Test if worker above wall
            if worker[1] + 1 == walls[i][1] and worker[0] == walls[i][0]:
                no_down = True
                
        
        if no_up == False:
            actions.append("up")
        if no_down == False:
            actions.append("down")
        if no_right == False:
            actions.append("right")
        if no_left == False:
           actions.append("left")
           
        return actions
   
    
        
        
        
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        #raise NotImplementedError
        # index of the blank
        next_state = list(state)  # Note that  next_state = state   would simply create an alias
        i_worker = state.worker  # index of the blank tile
        assert action in self.actions(state)  # defensive programming!
        
        if action == 'up':
            i_worker = tuple(i_worker(0), i_worker(1) - 1)
        elif action == 'down':
            i_worker = tuple(i_worker(0), i_worker(1) + 1)
        elif action == 'left':
            i_worker = tuple(i_worker(0) - 1, i_worker(1))
        elif action == 'right':
            i_worker = tuple(i_worker(0) + 1, i_worker(1))
        
        next_state.worker = i_worker
        
        return tuple(next_state)
        
    def goal_test(self, state, goal_coords = None):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        if goal_coords:
            return state.worker == goal_coords
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        #raise NotImplementedError
        return 1
  
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



def check_action_seq(warehouse, action_seq):
   
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object
    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Failure', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    for action in action_seq:
        if action == 'Left':
            #"Check if there's a box to the left"
            if ((warehouse.worker[0] - 1), (warehouse.worker[1])) in warehouse.boxes:
                #"Check if there's a box or wall to the left of that box"
                if ((warehouse.worker[0] - 2, warehouse.worker[1]) in warehouse.boxes) or \
                    ((warehouse.worker[0] - 2, warehouse.worker[1]) in warehouse.walls):
                        return "Failure"
                #"If there's empty space, move box and worker"
                else:
                    index = (warehouse.boxes).index((warehouse.worker[0]-1, warehouse.worker[1])) 
                    warehouse.boxes[index] = (warehouse.worker[0]-2, warehouse.worker[1])
                    warehouse.worker = (warehouse.worker[0]-1, warehouse.worker[1])
            #Check if there's a wall
            elif (warehouse.worker[0]-1, warehouse.worker[1]) in warehouse.walls:
                return "Failure"
            #"If it's just empty space, move worker to left"
            else:
                warehouse.worker = (warehouse.worker[0]-1, warehouse.worker[1])
        if action == 'Right':
            #"Check if there's a box to the right"
            if ((warehouse.worker[0] + 1), (warehouse.worker[1])) in warehouse.boxes:
                #"Check if there's a box or wall to the right of that box"
                if ((warehouse.worker[0] + 2, warehouse.worker[1]) in warehouse.boxes) or \
                    ((warehouse.worker[0] + 2, warehouse.worker[1]) in warehouse.walls):
                        return "Failure"
                #"If there's empty space, move box and worker"
                else:
                    index = (warehouse.boxes).index((warehouse.worker[0] + 1, warehouse.worker[1])) 
                    warehouse.boxes[index] = (warehouse.worker[0] + 2, warehouse.worker[1])
                    warehouse.worker = (warehouse.worker[0] + 1, warehouse.worker[1])
            #Check if there's a wall
            elif (warehouse.worker[0]+1, warehouse.worker[1]) in warehouse.walls:
                return "Failure"
            #"If it's just empty space, move worker to left"
            else:
                warehouse.worker = (warehouse.worker[0]+1, warehouse.worker[1])
        if action == 'Up':
            #"Check if there's a box above the worker"
            if ((warehouse.worker[0]), (warehouse.worker[1] - 1)) in warehouse.boxes:
                #"Check if there's a box or wall above that box"
                if (warehouse.worker[0], warehouse.worker[1] - 2) in warehouse.boxes or \
                    (warehouse.worker[0], warehouse.worker[1] - 2) in warehouse.walls:
                        return "Failure"
                #"If there's empty space, move box and worker"
                else:
                    index = (warehouse.boxes).index((warehouse.worker[0], warehouse.worker[1] - 1))
                    warehouse.boxes[index] = (warehouse.worker[0], warehouse.worker[1] - 2)
                    warehouse.worker = (warehouse.worker[0], warehouse.worker[1] - 1)
            #Check if there's a wall
            elif (warehouse.worker[0], warehouse.worker[1]-1) in warehouse.walls:
                return "Failure"
            #"If it's just empty space, move worker to left"
            else:
                warehouse.worker = (warehouse.worker[0], warehouse.worker[1]-1)
        if action == 'Down':
            #"Check if there's a box above the worker"
            if ((warehouse.worker[0]), (warehouse.worker[1] + 1)) in warehouse.boxes:
                #"Check if there's a box or wall above that box"
                if (warehouse.worker[0], warehouse.worker[1] + 2) in warehouse.boxes or \
                    (warehouse.worker[0], warehouse.worker[1] + 2) in warehouse.walls:
                        return "Failure"
                #"If there's empty space, move box and worker"
                else:
                    index = (warehouse.boxes).index((warehouse.worker[0], warehouse.worker[1] + 1))
                    warehouse.boxes[index] = (warehouse.worker[0], warehouse.worker[1] + 2)
                    warehouse.worker = (warehouse.worker[0], warehouse.worker[1] + 1)
            #Check if there's a wall
            elif (warehouse.worker[0], warehouse.worker[1]+1) in warehouse.walls:
                return "Failure"
            #"If it's just empty space, move worker to left"
            else:
                warehouse.worker = (warehouse.worker[0], warehouse.worker[1]+1)
                
    return warehouse.__str__()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using elementary actions 
    the puzzle defined in a file.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    search.breadth_first_tree_search(warehouse)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    
    
    ##         "INSERT YOUR CODE HERE"
    
    # Call calculate_path for warehouses and store in variable
    
    path_options = calculate_path(warehouse, dst)
    valid_paths = []
    is_failure = False
    # loop through path options and check legality, then check if boxes moved
    for path in path_options :
        for box in warehouse.boxes :
            if path == box:
                is_failure = True
        if is_failure == False:
            valid_paths.append(path)
        is_failure = False    
        
    if valid_paths  :
        return True
    else :
        return False

                
                
    # 
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
def calculate_path(warehouse, dst):
    '''
    Calculate all path options of worker to destination
    
    Return list of elementary actions needed for each path
    
    Return false if no paths available
    ''' 
    return search.breadth_first_graph_search_subfunc(warehouse, dst)
        
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):
    '''    
    Solve using macro actions the puzzle defined in the warehouse passed as
    a parameter. A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

