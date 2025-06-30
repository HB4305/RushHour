from collections import deque
import heapq
from logic import *

def bfs_solver(initial_state):
    visited = set()
    queue = deque()
    queue.append((initial_state, []))
    visited.add(state_key(initial_state))
    while queue:
        current_state, path = queue.popleft()
        if is_goal(current_state):
            return path + [current_state]
        for next_state in generate_moves(current_state):
            key = state_key(next_state)
            if key not in visited:
                visited.add(key)
                queue.append((next_state, path + [current_state]))
    return None

def dfs_solver(initial_state):
    visited = set()
    stack = []
    stack.append((initial_state, []))
    visited.add(state_key(initial_state))

    while stack:
        current_state, path = stack.pop()
        if is_goal(current_state):
            return path + [current_state]
        for next_state in generate_moves(current_state): # Nạp tất cả trạng thái có thể tiếp theo
            key = state_key(next_state)
            if key not in visited: # Chỉ thêm mới nếu chưa từng thăm
                visited.add(key)
                stack.append((next_state, path + [current_state]))
    return None

def ucs_solver(initial_state):
    visited = {}
    heap = []
    counter = 0  # Add counter to break ties
    # (total_cost, counter, path, state)
    heapq.heappush(heap, (0, counter, [], initial_state))
    visited[state_key(initial_state)] = 0
    counter += 1

    while heap:
        cost, _, path, current_state = heapq.heappop(heap)
        if is_goal(current_state):
            return path + [current_state]
        for next_state in generate_moves(current_state):
            # Find which vehicle moved and calculate cost
            move_cost = 1  # Default cost
            for name in current_state:
                if current_state[name][:2] != next_state[name][:2]:
                    vehicle_length = current_state[name][2]
                    steps_moved = 1  # Each move is exactly 1 step
                    move_cost = vehicle_length * steps_moved
                    break
            
            next_cost = cost + move_cost
            key = state_key(next_state)
            if key not in visited or next_cost < visited[key]:
                visited[key] = next_cost
                heapq.heappush(heap, (next_cost, counter, path + [current_state], next_state))
                counter += 1
    return None

def heuristic(state):
    if 'X' not in state:
        return float('inf')
    
    row, col, length, orient = state['X']
    
    if orient != 'H':  # Only horizontal cars can exit
        return float('inf')
    
    exit_distance = (5 - (col + length - 1))
    if exit_distance == 0:  # Already solved
        return 0
    
    blocking_cost = 0
    exit_path = range(col + length, 6)
    
    for c in exit_path:
        for name, (r, cl, l, o) in state.items():
            if name == 'X':
                continue
                
            # Vertical blocking car
            if o == 'V' and cl == c and r <= row < r + l:
                # Cost depends on how far the blocking car can move
                free_space_above = r  # Space to move up
                free_space_below = 5 - (r + l - 1)  # Space to move down
                min_moves_to_free = min(free_space_above, free_space_below) + 1
                blocking_cost += l * min_moves_to_free  # Longer cars need more moves
                break
                
            # Horizontal blocking car 
            elif o == 'H' and r == row and cl <= c < cl + l:
                
                free_space_left = cl
                free_space_right = 5 - (cl + l - 1)
                
                if free_space_left == 0 or free_space_right == 0:
                    blocking_cost += 10  # Need more times to moves
                else:
                    blocking_cost += 5  # Can move either side
                break
    
    
    return exit_distance + blocking_cost + (exit_distance * 0.1)

def a_star_solver(initial_state):
    from heapq import heappush, heappop

    if is_goal(initial_state):
        return [initial_state]


    counter = 0
    open_set = []
    initial_h = heuristic(initial_state)
    heappush(open_set, (initial_h, counter, 0, initial_state, [initial_state]))
    counter += 1

    visited = {}
    visited[state_key(initial_state)] = 0

    while open_set:
        _, _, g_score, current_state, path = heappop(open_set)

        if is_goal(current_state):
            return path

        for next_state in generate_moves(current_state):
            key = state_key(next_state)
            move_cost = 1  # base cost

            for name in current_state:
                if current_state[name] != next_state[name]:
                    move_cost = current_state[name][2]  
                    break

            new_g_score = g_score + move_cost

            if key not in visited or new_g_score < visited[key]:
                visited[key] = new_g_score
                f_score = new_g_score + heuristic(next_state)
                heappush(open_set, (f_score, counter, new_g_score, next_state, path + [next_state]))
                counter += 1

    return None

