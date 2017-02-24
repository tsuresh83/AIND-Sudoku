import operator
assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    #choose all boxes with 2 possible values
    unsolved = [b for b in boxes if len(values[b])==2]
    for us in unsolved:
        usUnits = units[us]
        #iterate through units of those potential twins
        for i in range(len(usUnits)):
            unit = usUnits[i]
            for us1 in unsolved:
                if us1 != us and us1 in unit and values[us1] == values[us]: # twin found
                    for c in values[us]:
                        for u in unit:
                            if u!=us and u !=us1: #eliminate values from all unit members
                                values[u] = values[u].replace(c,'')
                                assign_value(values,u,values[u])
    return values                      
                
    

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
            assign_value(values,peer,values[peer])
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
                assign_value(values,dplaces[0],digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        eliminate(values)
        only_choice(values)
        naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:
        return False
    if all(len(values[box])==1 for box in boxes):
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    cts = [[box,len(values[box])] for box in values.keys() if len(values[box]) > 1]
    sortedCts = sorted(cts,key=operator.itemgetter(1))
    smallestBox = sortedCts[0][0]
    smallestValues = values[smallestBox]
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for i in range(len(smallestValues)):
        valuesNew = values.copy()
        valuesNew[smallestBox] = smallestValues[i]
        ret = search(valuesNew)
        if ret :
            return ret


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    soln= search(grid_values(grid))
    if soln:
        return soln
    
rows = 'ABCDEFGHI'
cols = '123456789'


boxes = cross(rows, cols)
#assign boxes belonging to major and minor diagonals
major_diagonal = ['A1','B2','C3','D4','E5','F6','G7','H8','I9']
minor_diagonal = ['A9','B8','C7','D6','E5','F4','G3','H2','I1']
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#add major and minor diagonals to the unitlist - the rest of the logic will work as before
unitlist = row_units + column_units + square_units +[major_diagonal]+[minor_diagonal]
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
