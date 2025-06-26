import tkinter as tk
from tkinter import messagebox, simpledialog
from collections import deque
import copy
import random
import heapq
import time  
from PIL import Image, ImageTk  

# ===================== LOGIC =====================

def create_board(state):
    board = [['.' for _ in range(6)] for _ in range(6)]
    for name, (row, col, length, orient) in state.items():
        for i in range(length):
            r = row + i if orient == 'V' else row
            c = col + i if orient == 'H' else col
            board[r][c] = name
    return board

def state_key(state):
    return tuple(sorted((k, v[0], v[1]) for k, v in state.items()))

def is_goal(state):
    row, col, length, orient = state['X']
    if orient != 'H':
        return False
    end_col = col + length - 1
    if end_col > 5:
        return False
    for c in range(end_col + 1, 6):
        for name, (r, cc, l, o) in state.items():
            if name == 'X': continue
            for i in range(l):
                rr = r + i if o == 'V' else r
                rc = cc + i if o == 'H' else cc
                if rr == row and rc == c:
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


# ===================== MAPS =====================

maps = [
    {
        'X': (2, 0, 2, 'H'),
        'A': (0, 0, 2, 'V'),
        'B': (0, 1, 2, 'V'),
        'C': (0, 4, 3, 'V'),
        'D': (1, 5, 2, 'V'),
        'E': (3, 0, 3, 'H'),
        'F': (4, 3, 2, 'H'),
        'G': (5, 4, 2, 'H')
    },
    {
        'X': (2, 1, 2, 'H'),
        'A': (0, 0, 3, 'V'),
        'B': (0, 3, 2, 'V'),
        'C': (1, 5, 2, 'V'),
        'D': (3, 0, 3, 'H'),
        'E': (4, 2, 2, 'H'),
        'F': (5, 0, 2, 'H')
    },
    {
        'X': (2, 2, 2, 'H'),
        'A': (0, 0, 2, 'V'),
        'B': (0, 1, 2, 'V'),
        'C': (0, 3, 2, 'V'),
        'D': (1, 5, 2, 'V'),
        'E': (3, 0, 2, 'H'),
        'F': (4, 2, 3, 'H')
    },
    {
        'X': (2, 1, 2, 'H'),
        'A': (0, 0, 3, 'V'),
        'B': (0, 2, 2, 'V'),
        'C': (0, 3, 2, 'V'),
        'D': (1, 5, 2, 'V'),
        'E': (3, 1, 3, 'H'),
        'F': (4, 4, 2, 'H')
    },
    {
        'X': (2, 2, 2, 'H'),
        'A': (0, 0, 2, 'V'),
        'B': (0, 1, 2, 'V'),
        'C': (0, 4, 2, 'V'),
        'D': (1, 5, 2, 'V'),
        'E': (3, 3, 3, 'H'),
        'F': (4, 0, 2, 'H'),
        'G': (5, 3, 2, 'H')
    },
    {
        'X': (2, 1, 2, 'H'),
        'A': (0, 0, 2, 'V'),
        'B': (0, 3, 2, 'V'),
        'C': (0, 5, 2, 'V'),
        'D': (3, 0, 3, 'H'),
        'E': (4, 4, 2, 'H'),
        'F': (5, 1, 2, 'H')
    },
    {
        'X': (2, 0, 2, 'H'),
        'A': (0, 0, 2, 'V'),
        'B': (0, 1, 2, 'V'),
        'C': (0, 2, 3, 'V'),
        'D': (3, 0, 3, 'H'),
        'E': (4, 3, 2, 'H')
    },
    {
        'X': (2, 2, 2, 'H'),
        'A': (0, 0, 2, 'V'),
        'B': (0, 3, 2, 'V'),
        'C': (0, 5, 3, 'V'),
        'D': (3, 2, 3, 'H'),
        'E': (5, 2, 3, 'H')
    },
    {
        'X': (2, 1, 2, 'H'),
        'A': (0, 0, 3, 'V'),
        'B': (0, 3, 2, 'V'),
        'C': (0, 5, 3, 'V'),
        'D': (3, 0, 3, 'H'),
        'E': (3, 3, 3, 'H'),
        'F': (5, 2, 2, 'H')
    },
    {
        'X': (2, 0, 2, 'H'),
    }
]

# ===================== GUI =====================

CELL_SIZE = 130
BOARD_SIZE = 6
COLORS = {
    'X': '#FF4444', 'A': '#4444FF', 'B': '#44FF44', 'C': '#FF8844',
    'D': '#8844FF', 'E': '#FF44FF', 'F': '#44FFFF', 'G': '#8B4513',
    'H': '#FFD700', 'I': '#32CD32', 'J': '#FF69B4'
}

initial_state = {}
solution = []
step_index = 0
is_playing = False
has_solution = True
selected_algorithm = "BFS"  
solution_costs = []  # Store cumulative costs for UCS
animation_start_time = 0  # Start time when animation begins
current_animation_time = 0  # Current animation time
is_goal_reached = False  # Track if goal is reached
final_time = 0  # Store final completion time

def select_algorithm():
    global selected_algorithm
    
    # Create algorithm selection dialog
    dialog = tk.Toplevel()
    dialog.title("Chọn thuật toán")
    dialog.geometry("300x150")
    dialog.resizable(False, False)
    dialog.grab_set()  # Make dialog modal
    
    # Center the dialog
    dialog.transient(root)
    
    tk.Label(dialog, text="Chọn thuật toán giải Rush Hour:", font=("Arial", 12)).pack(pady=10)
    
    algorithm_var = tk.StringVar(value="BFS")
    
    tk.Radiobutton(dialog, text="BFS (Breadth-First Search)", variable=algorithm_var, value="BFS", font=("Arial", 10)).pack(anchor="w", padx=20)
    tk.Radiobutton(dialog, text="UCS (Uniform Cost Search)", variable=algorithm_var, value="UCS", font=("Arial", 10)).pack(anchor="w", padx=20)
    
    def confirm_selection():
        global selected_algorithm
        selected_algorithm = algorithm_var.get()
        dialog.destroy()
    
    tk.Button(dialog, text="Xác nhận", command=confirm_selection, 
              font=("Arial", 11, "bold"), bg="#FF44FF", fg="white", padx=30).pack(pady=10)
    
    # Wait for dialog to close
    dialog.wait_window()

def select_map():
    global initial_state
    
    # Create map selection dialog
    dialog = tk.Toplevel()
    dialog.title("Chọn bản đồ")
    dialog.geometry("400x400")
    dialog.resizable(False, False)
    dialog.grab_set()  # Make dialog modal
    
    # Center the dialog
    dialog.transient(root)
    
    tk.Label(dialog, text="Chọn bản đồ Rush Hour:", font=("Arial", 11, "bold")).pack(pady=10)
    
    # Create a frame for map selection with scrollbar
    frame = tk.Frame(dialog)
    frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    map_var = tk.StringVar(value="0")
    
    # Create radio buttons for all 10 maps
    for i, map_data in enumerate(maps):
        # Create a description for each map
        vehicle_count = len(map_data)
        truck_count = sum(1 for v in map_data.values() if v[2] == 3)  # Count vehicles with length 3
        car_count = vehicle_count - truck_count - 1  # Subtract trucks and red car X
        
        description = f"Bản đồ {i+1}"
        
        tk.Radiobutton(frame, text=description, variable=map_var, value=str(i), 
                      font=("Arial", 9), anchor="w").pack(anchor="w", pady=2)
    
    selected_map = None
    
    def confirm_selection():
        nonlocal selected_map
        selection = map_var.get()
        selected_map = maps[int(selection)]
        dialog.destroy()
    
    
    # Buttons frame
    btn_frame = tk.Frame(dialog)
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="Xác nhận", command=confirm_selection, 
              font=("Arial", 10, "bold"), bg="#FF44FF", fg="white", padx=30).pack(side=tk.LEFT, padx=10)
    
    # Wait for dialog to close
    dialog.wait_window()
    
    return selected_map

def load_new_map():
    global initial_state, solution, step_index, has_solution, solution_costs, animation_start_time, current_animation_time, is_goal_reached, final_time
    
    # Get selected map
    selected_map = select_map()
    if selected_map:
        initial_state = selected_map
    else:
        # Fallback to first valid map
        initial_state = maps[0]
    
    # Reset timer variables
    animation_start_time = 0
    current_animation_time = 0
    is_goal_reached = False
    final_time = 0
    
    # Use selected algorithm
    if selected_algorithm == "BFS":
        result = bfs_solver(initial_state)
        solution_costs = []  # BFS doesn't need cost tracking
    else: # UCS
        result = ucs_solver(initial_state)
        if result:
            # Calculate cumulative costs for UCS display
            solution_costs = [0]  # Initial state has cost 0
            for i in range(1, len(result)):
                prev_state = result[i-1]
                curr_state = result[i]
                # Find which vehicle moved and calculate cost
                move_cost = 1  # Default
                for name in prev_state:
                    if prev_state[name][:2] != curr_state[name][:2]:
                        vehicle_length = prev_state[name][2]
                        move_cost = vehicle_length * 1  # length * 1 step
                        break
                solution_costs.append(solution_costs[-1] + move_cost)
        else:
            solution_costs = []
    
    if result is None:
        solution = [initial_state]
        has_solution = False
    else:
        solution = result
        has_solution = True
    step_index = 0

def update_timer():
    global current_animation_time, is_goal_reached, final_time
    
    if is_playing and animation_start_time > 0 and not is_goal_reached:
        current_animation_time = time.time() - animation_start_time
        
        # Update display first
        draw_board()
        
        # Continue updating if still playing and not reached goal
        if is_playing and not is_goal_reached:
            root.after(50, update_timer)  # Update every 50ms for smooth display

def load_background():
    """Load background image for the game board"""
    try:
        # Try to load background image
        bg_path = "image/background.png"  # You can change this path
        bg_image = Image.open(bg_path)
        bg_image = bg_image.resize((CELL_SIZE * BOARD_SIZE, CELL_SIZE * BOARD_SIZE), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(bg_image)
    except FileNotFoundError:
        print("Background image not found, using default background")
        return None

def load_car_images():
    """Load car images for all vehicles"""
    car_images = {}
    try:
        # Load images for each car and orientation
        for name in ['X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
            for orient in ['H', 'V']:
                # Load images for different possible lengths (2 and 3)
                for length in [2, 3]:
                    try:
                        # Try to load specific car image with length
                        img_path = f"image/{name}_{orient}.png"  # e.g., "X_H.png", "A_V.png"
                        car_img = Image.open(img_path)
                        
                        # Calculate size based on orientation and length
                        if orient == 'H':
                            width = CELL_SIZE * length
                            height = CELL_SIZE
                        else:
                            width = CELL_SIZE
                            height = CELL_SIZE * length
                        
                        car_img = car_img.resize((width, height), Image.Resampling.LANCZOS)
                        car_images[f"{name}_{orient}_{length}"] = ImageTk.PhotoImage(car_img)
                        
                    except FileNotFoundError:
                        continue
                        
    except Exception as e:
        print(f"Error loading car images: {e}")
    
    return car_images

def draw_board():
    global canvas, solution, step_index, info_label, algorithm_label, time_label, background_image, car_images
    canvas.delete("all")

    # Draw background image or fallback to grid
    if background_image:
        canvas.create_image(0, 0, anchor="nw", image=background_image)
    else:
        # Fallback: Draw grid background if no image
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x0 = c * CELL_SIZE
                y0 = r * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
                canvas.create_rectangle(x0, y0, x1, y1, fill="#F0F0F0", outline="#CCCCCC", width=1)

    # Draw exit arrow
    exit_x = 5 * CELL_SIZE + CELL_SIZE - 5
    exit_y = 2 * CELL_SIZE + CELL_SIZE // 2
    canvas.create_polygon(exit_x, exit_y - 10, exit_x + 15, exit_y, exit_x, exit_y + 10, 
                         fill="red", outline="darkred", width=2)

    if solution:
        state = solution[step_index]
        for name, (row, col, length, orient) in state.items():
            x0 = col * CELL_SIZE
            y0 = row * CELL_SIZE
            
            # Try to use car image first with actual length from state
            car_key = f"{name}_{orient}_{length}"  # Use actual length from state
            if car_images and car_key in car_images:
                # Use car image
                canvas.create_image(x0, y0, anchor="nw", image=car_images[car_key])
                
                # Add car label on top of image
                if orient == 'H':
                    cx = x0 + (length * CELL_SIZE) // 2
                    cy = y0 + CELL_SIZE // 2
                else:
                    cx = x0 + CELL_SIZE // 2
                    cy = y0 + (length * CELL_SIZE) // 2
                
                # canvas.create_text(cx, cy, text=name, font=("Arial", 16, "bold"), fill="hotpink")
            else:
                # Fallback to drawing cars manually if no image
                x1 = (col + length) * CELL_SIZE if orient == 'H' else x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE if orient == 'H' else (row + length) * CELL_SIZE

                color = COLORS.get(name, "#808080")
                shadow_color = "#333333"
                
                # Add some padding for better visual
                padding = 5
                
                if orient == 'H':
                    # Horizontal car
                    car_x0 = x0 + padding
                    car_y0 = y0 + padding
                    car_x1 = x1 - padding
                    car_y1 = y1 - padding
                    
                    # Car shadow
                    canvas.create_rectangle(car_x0 + 2, car_y0 + 2, car_x1 + 2, car_y1 + 2, 
                                          fill=shadow_color, outline="")
                    
                    # Main car body
                    canvas.create_rectangle(car_x0, car_y0, car_x1, car_y1, 
                                          fill=color, outline="black", width=2)
                    
                    # Car roof (smaller rectangle on top)
                    roof_height = (car_y1 - car_y0) // 3
                    canvas.create_rectangle(car_x0 + 10, car_y0, car_x1 - 10, car_y0 + roof_height,
                                          fill=color, outline="black", width=1)
                    
                    # Windscreen
                    canvas.create_rectangle(car_x0 + 15, car_y0 + 5, car_x1 - 15, car_y0 + roof_height - 5,
                                          fill="#E6E6FA", outline="black", width=1)
                    
                    # Front and rear lights
                    canvas.create_oval(car_x1 - 8, car_y0 + 5, car_x1 - 3, car_y0 + 15, fill="white", outline="black")
                    canvas.create_oval(car_x0 + 3, car_y0 + 5, car_x0 + 8, car_y0 + 15, fill="yellow", outline="black")
                    
                    # Wheels
                    wheel_y = car_y1 - 12
                    canvas.create_oval(car_x0 + 8, wheel_y, car_x0 + 18, car_y1 - 2, fill="black", outline="gray", width=2)
                    canvas.create_oval(car_x1 - 18, wheel_y, car_x1 - 8, car_y1 - 2, fill="black", outline="gray", width=2)
                    
                    # Wheel rims
                    canvas.create_oval(car_x0 + 11, wheel_y + 3, car_x0 + 15, car_y1 - 5, fill="silver")
                    canvas.create_oval(car_x1 - 15, wheel_y + 3, car_x1 - 11, car_y1 - 5, fill="silver")
                    
                else:
                    # Vertical car
                    car_x0 = x0 + padding
                    car_y0 = y0 + padding
                    car_x1 = x1 - padding
                    car_y1 = y1 - padding
                    
                    # Car shadow
                    canvas.create_rectangle(car_x0 + 2, car_y0 + 2, car_x1 + 2, car_y1 + 2, 
                                          fill=shadow_color, outline="")
                    
                    # Main car body
                    canvas.create_rectangle(car_x0, car_y0, car_x1, car_y1, 
                                          fill=color, outline="black", width=2)
                    
                    # Car roof (smaller rectangle on top)
                    roof_width = (car_x1 - car_x0) // 3
                    canvas.create_rectangle(car_x0, car_y0 + 10, car_x0 + roof_width, car_y1 - 10,
                                          fill=color, outline="black", width=1)
                    
                    # Windscreen
                    canvas.create_rectangle(car_x0 + 5, car_y0 + 15, car_x0 + roof_width - 5, car_y1 - 15,
                                          fill="#E6E6FA", outline="black", width=1)
                    
                    # Front and rear lights
                    canvas.create_oval(car_x0 + 5, car_y0 + 3, car_x0 + 15, car_y0 + 8, fill="white", outline="black")
                    canvas.create_oval(car_x0 + 5, car_y1 - 8, car_x0 + 15, car_y1 - 3, fill="yellow", outline="black")
                    
                    # Wheels
                    wheel_x = car_x1 - 12
                    canvas.create_oval(wheel_x, car_y0 + 8, car_x1 - 2, car_y0 + 18, fill="black", outline="gray", width=2)
                    canvas.create_oval(wheel_x, car_y1 - 18, car_x1 - 2, car_y1 - 8, fill="black", outline="gray", width=2)
                    
                    # Wheel rims
                    canvas.create_oval(wheel_x + 3, car_y0 + 11, car_x1 - 5, car_y0 + 15, fill="silver")
                    canvas.create_oval(wheel_x + 3, car_y1 - 15, car_x1 - 5, car_y1 - 11, fill="silver")

                # Car label
                cx = (x0 + x1) // 2
                cy = (y0 + y1) // 2
                canvas.create_text(cx, cy, text=name, font=("Arial", 16, "bold"), fill="hotpink")

        if has_solution:
            if selected_algorithm == "BFS":
                info_label.config(text=f"Step {step_index}    Total cost: {step_index}", fg="black")
            else: 
                current_cost = solution_costs[step_index] if step_index < len(solution_costs) else 0
                info_label.config(text=f"Step {step_index}    Total cost: {current_cost}", fg="black")
            algorithm_label.config(text=f"Thuật toán: {selected_algorithm}")
            
            # Update time display with smooth animation
            if is_goal_reached:
                time_label.config(text=f"🎉 HOÀN THÀNH! Thời gian: {final_time:.2f}s", fg="green")
            elif is_playing and animation_start_time > 0:
                time_label.config(text=f"⏱️ Đang chạy: {current_animation_time:.2f}s", fg="blue")
            elif animation_start_time > 0:  # Paused but has started
                time_label.config(text=f"⏸️ Tạm dừng: {current_animation_time:.2f}s", fg="orange")
            else:
                time_label.config(text="", fg="green")
        else:
            info_label.config(text="🚫 No solution found.", fg="red")
            algorithm_label.config(text=f"Thuật toán: {selected_algorithm} - Không có lời giải")
            time_label.config(text="Không có lời giải", fg="red")

def next_step():
    global step_index, is_goal_reached, final_time, is_playing
    if solution and step_index < len(solution) - 1:
        step_index += 1
        
        # Check for goal immediately after stepping
        if solution and step_index < len(solution):
            state = solution[step_index]
            if 'X' in state:
                row, col, length, orient = state['X']
                if orient == 'H' and col + length - 1 == 5:
                    is_goal_reached = True
                    if animation_start_time > 0:
                        final_time = time.time() - animation_start_time
                    is_playing = False
                    play_button.config(text="Play")
        
        draw_board()

def prev_step():
    global step_index
    if solution and step_index > 0:
        step_index -= 1
        draw_board()

def reset_step():
    global step_index, is_playing, animation_start_time, current_animation_time, is_goal_reached, final_time
    is_playing = False
    animation_start_time = 0
    current_animation_time = 0
    is_goal_reached = False
    final_time = 0
    play_button.config(text="Play")
    select_algorithm()  # Show algorithm selection dialog
    load_new_map()  # This will now show map selection dialog
    draw_board()

def toggle_play():
    global is_playing, animation_start_time, current_animation_time, is_goal_reached
    if not has_solution:
        messagebox.showwarning("Không thể giải", " Bản đồ này không có lời giải!\nHãy bấm Reset để chọn bản đồ khác.")
        return
    
    is_playing = not is_playing
    play_button.config(text="Pause" if is_playing else "Play")
    
    if is_playing:
        if step_index == 0 and not is_goal_reached:  # Starting animation
            animation_start_time = time.time()
            current_animation_time = 0
        elif animation_start_time > 0:  # Resume from pause
            # Adjust start time to account for paused duration
            animation_start_time = time.time() - current_animation_time
        update_timer()  # Start smooth timer
        auto_step()
    else:
        # Paused - keep current time but stop auto-stepping
        draw_board()  # Update display to show paused state

def auto_step():
    global is_playing, is_goal_reached, final_time
    if is_playing and solution and step_index < len(solution) - 1 and not is_goal_reached:
        next_step()
        
        # Check goal immediately after next_step
        if solution and step_index < len(solution):
            state = solution[step_index]
            if 'X' in state:
                row, col, length, orient = state['X']
                if orient == 'H' and col + length - 1 == 5:
                    is_goal_reached = True
                    if animation_start_time > 0:
                        final_time = time.time() - animation_start_time
                    is_playing = False
                    play_button.config(text="Play")
                    return  # Exit immediately when goal is reached
        
        if not is_goal_reached and is_playing:  # Only continue if goal not reached and still playing
            root.after(700, auto_step)
    else:
        is_playing = False
        play_button.config(text="Play")

def quit_program():
    import sys
    root.quit()
    root.destroy()
    sys.exit()

def main():
    """Main function to initialize and run the Rush Hour game"""
    global root, canvas, info_label, algorithm_label, time_label, play_button
    global background_image, car_images
    
    # Create main window
    root = tk.Tk()
    root.title("Rush Hour - Algorithm Solver")
    
    # Show algorithm selection dialog on startup
    select_algorithm()
    
    # Load images
    background_image = load_background()
    car_images = load_car_images()
    
    # Create canvas
    canvas = tk.Canvas(root, width=CELL_SIZE * BOARD_SIZE, height=CELL_SIZE * BOARD_SIZE)
    canvas.pack()
    
    # Create info labels
    info_label = tk.Label(root, text="", font=("Arial", 12))
    info_label.pack()
    
    algorithm_label = tk.Label(root, text=f"Thuật toán: {selected_algorithm}", font=("Arial", 10), fg="blue")
    algorithm_label.pack()
    
    time_label = tk.Label(root, text="", font=("Arial", 10), fg="green")
    time_label.pack()
    
    # Create button frame
    btn_frame = tk.Frame(root)
    btn_frame.pack()
    
    # Create buttons
    tk.Button(btn_frame, text="<< Prev", command=prev_step).pack(side=tk.LEFT, padx=5)
    play_button = tk.Button(btn_frame, text="Play", command=toggle_play)
    play_button.pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Next >>", command=next_step).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Reset", command=reset_step).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Quit", command=quit_program, bg="#f44336", fg="white").pack(side=tk.LEFT, padx=5)
    
    # Load initial map and start the game
    load_new_map()
    draw_board()
    
    # Start the main loop
    root.mainloop()

# ===================== MAIN =====================

if __name__ == "__main__":
    main()
