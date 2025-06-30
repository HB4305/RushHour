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
    """Heuristic function for A* - estimates distance to goal"""
    if 'X' not in state:
        return float('inf')
    
    # red car position
    row, col, length, orient = state['X']
    
    if orient == 'H':
        # For horizontal car, distance is number of blocks to exit (column 5)
        distance = (5 - (col + length - 1))
        
        # Check if path to exit is blocked
        blocking_cars = 0
        exit_row = row
        for c in range(col + length, 6):
            for name, (r, cl, l, o) in state.items():
                if o == 'V' and cl == c and r <= exit_row < r + l:
                    blocking_cars += l * 2
                    break
                elif o == 'H' and r == exit_row and cl <= c < cl + l:
                    blocking_cars += 3
                    break
        
        # Heuristic is distance + number of blocking cars
        return distance + blocking_cars
    else:
        # Vertical car can't exit
        return float('inf')

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

