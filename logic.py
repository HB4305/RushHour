import copy

def create_board(state):
    board = [['.' for _ in range(6)] for _ in range(6)] # Create a 6x6 board filled with '.'
    for name, (row, col, length, orient) in state.items(): # Get information of each car
        for i in range(length): # Mark each cell occupied by the car
            r = row + i if orient == 'V' else row # Increase row for vertical cars
            c = col + i if orient == 'H' else col # Increase column for horizontal cars
            board[r][c] = name # Mark the cell with the car's name
    return board

def state_key(state):
    return tuple(sorted((k, v[0], v[1]) for k, v in state.items())) 
    # Only keep the name, the position (row, col) of each car
    # Typecast to tuple for immutability and sorting for consistent order

def is_goal(state):
    row, col, length, orient = state['X']
    if orient != 'H':
        return False
    end_col = col + length - 1
    if end_col > 5:
        return False
    
# Check if the exit is clear
    for name, (r, c, l, o) in state.items():
        if name == 'X': continue
        for i in range(l):
            rr = r + i if o == 'V' else r
            cc = c + i if o == 'H' else c 
            if rr == row and cc in range(end_col + 1, 6): # If any other car blocks the exit
                return False
    return end_col == 5

def generate_moves(state):
    board = create_board(state)
    next_states = []
    for name, (row, col, length, orient) in state.items():
        if orient == 'H':
            if col > 0 and board[row][col - 1] == '.':
                new_state = copy.deepcopy(state)
                new_state[name] = (row, col - 1, length, orient)
                next_states.append(new_state)
            if col + length < 6 and board[row][col + length] == '.':
                new_state = copy.deepcopy(state)
                new_state[name] = (row, col + 1, length, orient)
                next_states.append(new_state)
        else:
            if row > 0 and board[row - 1][col] == '.':
                new_state = copy.deepcopy(state)
                new_state[name] = (row - 1, col, length, orient)
                next_states.append(new_state)
            if row + length < 6 and board[row + length][col] == '.':
                new_state = copy.deepcopy(state)
                new_state[name] = (row + 1, col, length, orient)
                next_states.append(new_state)
    return next_states