import tkinter as tk
from tkinter import messagebox
from collections import deque
import copy
import random
import heapq
# # from PIL import Image, ImageTk

# CELL_SIZE = 80
# BOARD_SIZE = 6
# # ===================== LOAD IMAGES ====================
# # def load_images():
# #     imgs = {}
# #     for name in ['X','A','B','C','D','E','F','G']:
# #         for o in ['H','V']:
# #             fname = f"{name}_{o}.png"
# #             path = os.path.join("images", fname)
# #             if os.path.exists(path):
# #                 # Xác định chiều dài: xe C giả định dài 3; tùy map
# #                 length = 3 if name in ['C','E'] else 2
# #                 w = CELL_SIZE * length if o=='H' else CELL_SIZE
# #                 h = CELL_SIZE if o=='H' else CELL_SIZE * length
# #                 img = Image.open(path).resize((w,h), Image.ANTIALIAS)
# #                 # img = Image.open(path).resize((w, h), Image.Resampling.LANCZOS)

# #                 imgs[f"{name}_{o}"] = ImageTk.PhotoImage(img)
# #     return imgs

# # images = {}
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
            # Find which vehicle moved
            for name in current_state:
                if current_state[name][:2] != next_state[name][:2]:
                    move_cost = current_state[name][2]  # length of vehicle
                    break
            else:
                move_cost = 0
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
        'A': (0, 0, 3, 'V'),
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
    }
]

# ===================== GUI =====================

CELL_SIZE = 80
BOARD_SIZE = 6
COLORS = {
    'X': 'red', 'A': 'blue', 'B': 'green', 'C': 'orange',
    'D': 'purple', 'E': 'pink', 'F': 'cyan', 'G': 'brown'
}

initial_state = {}
solution = []
step_index = 0
is_playing = False
has_solution = True

def load_new_map():
    global initial_state, solution, step_index, has_solution
    initial_state = random.choice(maps)
    result = bfs_solver(initial_state)
    if result is None:
        solution = [initial_state]
        has_solution = False
    else:
        solution = result
        has_solution = True
    step_index = 0

def draw_board():
    global canvas, solution, step_index, info_label
    canvas.delete("all")

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            x0 = c * CELL_SIZE
            y0 = r * CELL_SIZE
            x1 = x0 + CELL_SIZE
            y1 = y0 + CELL_SIZE
            canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="lightgray")

    if solution:
        state = solution[step_index]
        for name, (row, col, length, orient) in state.items():
            x0 = col * CELL_SIZE
            y0 = row * CELL_SIZE
            x1 = (col + length) * CELL_SIZE if orient == 'H' else x0 + CELL_SIZE
            y1 = y0 + CELL_SIZE if orient == 'H' else (row + length) * CELL_SIZE

            color = COLORS.get(name, "gray")

            if length == 2:
                if orient == 'H':
                    canvas.create_rectangle(x0 + 10, y0, x1 - 10, y1, fill=color, outline="black", width=2)
                    canvas.create_arc(x0, y0, x0 + 20, y1, start=90, extent=180, fill=color, outline="black")
                    canvas.create_arc(x1 - 20, y0, x1, y1, start=270, extent=180, fill=color, outline="black")
                else:
                    canvas.create_rectangle(x0, y0 + 10, x1, y1 - 10, fill=color, outline="black", width=2)
                    canvas.create_arc(x0, y0, x1, y0 + 20, start=180, extent=180, fill=color, outline="black")
                    canvas.create_arc(x0, y1 - 20, x1, y1, start=0, extent=180, fill=color, outline="black")
            else:
                canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black", width=2)

            # Cửa sổ
            cx = (x0 + x1) // 2
            cy = (y0 + y1) // 2
            canvas.create_rectangle(cx - 10, cy - 10, cx + 10, cy + 10, fill="white", outline="black")

            # Bánh xe
            if orient == 'H':
                canvas.create_oval(x0 + 5, y1 - 10, x0 + 15, y1, fill="black")
                canvas.create_oval(x1 - 15, y1 - 10, x1 - 5, y1, fill="black")
            else:
                canvas.create_oval(x0, y1 - 15, x0 + 10, y1 - 5, fill="black")
                canvas.create_oval(x1 - 10, y1 - 15, x1, y1 - 5, fill="black")

            # Tên xe
            canvas.create_text(cx, cy, text=name, font=("Arial", 20, "bold"))
#             # key = f"{name}_{orient}"
#             # img = images.get(key)
#             # if img:
#             #     canvas.create_image(x0, y0, anchor='nw', image=img)
#             # else:
#             #   # fallback nếu không có ảnh
#             #     canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black", width=2)
#             #     canvas.create_text((x0+x1)//2, (y0+y1)//2, text=name, font=("Arial", 20, "bold"))

#             #     # Cửa sổ
#             #     cx = (x0 + x1) // 2
#             #     cy = (y0 + y1) // 2
#             #     canvas.create_rectangle(cx - 10, cy - 10, cx + 10, cy + 10, fill="white", outline="black")

#             #     # Bánh xe
#             #     if orient == 'H':
#             #         canvas.create_oval(x0 + 5, y1 - 10, x0 + 15, y1, fill="black")
#             #         canvas.create_oval(x1 - 15, y1 - 10, x1 - 5, y1, fill="black")
#             #     else:
#             #         canvas.create_oval(x0, y1 - 15, x0 + 10, y1 - 5, fill="black")
#             #         canvas.create_oval(x1 - 10, y1 - 15, x1, y1 - 5, fill="black")

#             #     # Tên xe
#             #     canvas.create_text(cx, cy, text=name, font=("Arial", 20, "bold"))

#             # if has_solution:
#             #     info_label.config(text=f"Step {step_index}/{len(solution)-1}    Total cost: {step_index}", fg="black")
#             # else:
#             #     info_label.config(text="🚫 No solution found.", fg="red")

        if has_solution:
            info_label.config(text=f"Step {step_index}/{len(solution)-1}    Total cost: {step_index}", fg="black")
        else:
            info_label.config(text="🚫 No solution found.", fg="red")

def next_step():
    global step_index
    if solution and step_index < len(solution) - 1:
        step_index += 1
        draw_board()

def prev_step():
    global step_index
    if solution and step_index > 0:
        step_index -= 1
        draw_board()

def reset_step():
    global step_index, is_playing
    is_playing = False
    play_button.config(text="Play")
    load_new_map()
    draw_board()

def toggle_play():
    global is_playing
    if not has_solution:
        messagebox.showwarning("Không thể giải", " Bản đồ này không có lời giải!\nHãy bấm Reset để chọn bản đồ khác.")
        return
    is_playing = not is_playing
    play_button.config(text="Pause" if is_playing else "Play")
    if is_playing:
        auto_step()

def auto_step():
    global is_playing
    if is_playing and solution and step_index < len(solution) - 1:
        next_step()
        root.after(700, auto_step)
    else:
        is_playing = False
        play_button.config(text="Play")

# ===================== MAIN =====================

root = tk.Tk()
root.title("Rush Hour - BFS GUI")

canvas = tk.Canvas(root, width=CELL_SIZE * BOARD_SIZE, height=CELL_SIZE * BOARD_SIZE)
canvas.pack()

info_label = tk.Label(root, text="", font=("Arial", 12))
info_label.pack()

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="<< Prev", command=prev_step).pack(side=tk.LEFT, padx=5)
play_button = tk.Button(btn_frame, text="Play", command=toggle_play)
play_button.pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Next >>", command=next_step).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Reset", command=reset_step).pack(side=tk.LEFT, padx=5)

# # images = load_images()  # Load ảnh PNG
load_new_map()
draw_board()
root.mainloop()
