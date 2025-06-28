import copy

def create_board(state):
    board = [['.' for _ in range(6)] for _ in range(6)] # Tạo bảng 6x6
    for name, (row, col, length, orient) in state.items(): # lấy trạng thái từng xe
        for i in range(length): # đánh dấu từng ô thuộc xe
            r = row + i if orient == 'V' else row # tăng theo chiều dọc
            c = col + i if orient == 'H' else col #tăng theo chiều ngang
            board[r][c] = name # Đánh dấu 1 ô của xe
            # if orient == 'V':
            #     board[row + i][col] = name # Đánh dấu 1 ô của xe
            # else: # == 'H'
            #     board[row][col + i] = name
            
    return board

def state_key(state):
    return tuple(sorted((k, v[0], v[1]) for k, v in state.items())) 
    # Chỉ lấy tên xe, hàng, cột là đủ thông tin
    # ép về tuple để có thể hash (set, dict)

def is_goal(state):
    row, col, length, orient = state['X']
    if orient != 'H':
        return False
    end_col = col + length - 1
    if end_col > 5:
        return False
    #for c in range(end_col + 1, 6):
    for name, (r, cc, l, o) in state.items():
        if name == 'X': continue
        for i in range(l):
            rr = r + i if o == 'V' else r
            rc = cc + i if o == 'H' else cc
            #if rr == row and rc == c, muốn đổi tên biến c 
            if rr == row and rc in range(end_col + 1, 6): # gọn hơn vì mỗi xe lặp 1 lần
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