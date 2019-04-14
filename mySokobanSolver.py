
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
    return [ (9683836, 'Rafael', 'Alves'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


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
        raise NotImplementedError
    
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
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()


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
    
    raise NotImplementedError()

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
    
    raise NotImplementedError()

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

