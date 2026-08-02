# visual_grid_game.py
import random
import tkinter as tk

class VisualGridHuntGame:
    """A flexible Pacman-style grid environment with support for configurable opponents, larger scales, and traps."""

    def __init__(self, width=10, height=10, num_food=10, num_opponents=2, custom_walls=None):
        self.width = width
        self.height = height
        self.agent_pos = [0, 0]  # Starting position (x, y)
        self.agent_direction = 'Up'

        if custom_walls is not None:
            self.walls = set(custom_walls)
        else:
            self.walls = {(2, 2), (2, 3), (5, 5), (6, 5), (3, 7)}

        self.food_positions = set()
        while len(self.food_positions) < num_food:
            fx = random.randint(0, self.width - 1)
            fy = random.randint(0, self.height - 1)
            pos_tuple = (fx, fy)
            if pos_tuple != (0, 0) and pos_tuple not in self.walls:
                self.food_positions.add(pos_tuple)

        self.opponents = []
        while len(self.opponents) < num_opponents:
            ox = random.randint(0, self.width - 1)
            oy = random.randint(0, self.height - 1)
            op_pos = [ox, oy]
            if tuple(op_pos) != (0, 0) and tuple(op_pos) not in self.walls and tuple(op_pos) not in self.food_positions:
                self.opponents.append(op_pos)

        self.toxic_traps = set()
        num_traps = 4
        while len(self.toxic_traps) < num_traps:
            tx = random.randint(0, self.width - 1)
            ty = random.randint(0, self.height - 1)
            t_pos = (tx, ty)
            if (t_pos != (0, 0) and t_pos not in self.walls and 
                t_pos not in self.food_positions and list(t_pos) not in self.opponents):
                self.toxic_traps.add(t_pos)

        self.score = 0
        self.steps = 0
        self.collision = False

    def get_percept(self) -> dict:
        """Local sensing for partial observability."""
        x, y = self.agent_pos
        food_here = (x, y) in self.food_positions
        toxin_here = (x, y) in self.toxic_traps
        
        next_x, next_y = x, y
        if self.agent_direction == 'Up': next_y += 1
        elif self.agent_direction == 'Down': next_y -= 1
        elif self.agent_direction == 'Left': next_x -= 1
        elif self.agent_direction == 'Right': next_x += 1
            
        is_out_of_bounds = next_x < 0 or next_x >= self.width or next_y < 0 or next_y >= self.height
        wall_ahead = is_out_of_bounds or (next_x, next_y) in self.walls
        opponent_ahead = [next_x, next_y] in self.opponents
        
        return {
            'food_here': food_here,
            'toxin_here': toxin_here,
            'wall_ahead': wall_ahead,
            'opponent_ahead': opponent_ahead,
            'collision': self.collision
        }

    def execute_action(self, action: str):
        self.steps += 1
        new_pos = list(self.agent_pos)

        if action in ['Up', 'Down', 'Left', 'Right']:
            self.agent_direction = action

        if action == 'Up': new_pos[1] = min(self.height - 1, new_pos[1] + 1)
        elif action == 'Down': new_pos[1] = max(0, new_pos[1] - 1)
        elif action == 'Left': new_pos[0] = max(0, new_pos[0] - 1)
        elif action == 'Right': new_pos[0] = min(self.width - 1, new_pos[0] + 1)

        if tuple(new_pos) in self.walls:
            self.score -= 5
        else:
            self.agent_pos = new_pos

        tuple_pos = tuple(self.agent_pos)
        
        if tuple_pos in self.food_positions:
            self.food_positions.remove(tuple_pos)
            self.score += 20
            
        if tuple_pos in self.toxic_traps:
            self.score -= 15
            self.toxic_traps.remove(tuple_pos)

        for op in self.opponents:
            move = random.choice(['Up', 'Down', 'Left', 'Right', 'Stay'])
            if move == 'Up' and op[1] < self.height - 1: op[1] += 1
            elif move == 'Down' and op[1] > 0: op[1] -= 1
            elif move == 'Left' and op[0] > 0: op[0] -= 1
            elif move == 'Right' and op[0] < self.width - 1: op[0] += 1

            if op == self.agent_pos:
                self.score -= 50
                self.collision = True

    def is_done(self) -> bool:
        return len(self.food_positions) == 0 or self.steps >= 60 or self.collision


# ==========================================
# AGENT ARCHITECTURES
# ==========================================

class SimpleReflexAgent:
    """An agent that acts solely on the current percept, with no memory."""
    def sense_and_act(self, percept):
        if percept['toxin_here']:
            return 'Down'
        elif percept['wall_ahead'] or percept['opponent_ahead']:
            return 'Left'
        else:
            return 'Up'

class ModelBasedAgent:
    """An agent that maintains internal state to avoid getting stuck in loops."""
    
    def __init__(self):
        # Memory to track the current state of the agent
        self.last_action = None
        self.stuck_counter = 0  # Tracks how many times we've hit consecutive walls

    def sense_and_act(self, percept):
        # 1. Update State (Transition Model)
        if percept['wall_ahead']:
            self.stuck_counter += 1
        else:
            self.stuck_counter = 0  # Reset if the path is clear

        # 2. Decision Logic based on Percept + Memory
        if percept['toxin_here']:
            action = 'Down'
            
        elif percept['wall_ahead'] or percept['opponent_ahead']:
            # Querying memory: Have I already tried turning left and hit a wall again?
            if self.stuck_counter > 1:
                action = 'Right'  # Break the loop by trying a new direction
                self.stuck_counter = 0  # Reset memory after taking evasion action
            else:
                action = 'Left'
                
        else:
            action = 'Up'

        # 3. Save the action to memory for the next cycle
        self.last_action = action
        return action
# ==========================================
# GUI AND MAIN LOOP
# ==========================================

class GridGameGUI:
    def __init__(self, root, width=10, height=10, num_food=12, num_opponents=2, walls=None):
        self.root = root
        self.root.title("IT3012 - Scalable Multi-Agent Grid Hunt")
        self.env = VisualGridHuntGame(width=width, height=height, num_food=num_food, num_opponents=num_opponents, custom_walls=walls)

        max_canvas_dim = 600
        self.cell_size = max(20, min(max_canvas_dim // self.env.width, max_canvas_dim // self.env.height))

        canvas_w = self.env.width * self.cell_size
        canvas_h = self.env.height * self.cell_size

        self.canvas = tk.Canvas(root, width=canvas_w, height=canvas_h, bg="white")
        self.canvas.pack()

        self.label = tk.Label(root, text="Score: 0 | Steps: 0", font=("Arial", 14))
        self.label.pack(pady=10)

        self.btn = tk.Button(root, text="Start Simulation", command=self.run_loop, font=("Arial", 12), bg="#000066", fg="white")
        self.btn.pack(pady=5)

        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for x in range(self.env.width):
            for y in range(self.env.height):
                x1 = x * self.cell_size
                y1 = (self.env.height - 1 - y) * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "#f1f5f9" if (x, y) not in self.env.walls else "#64748b"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#cbd5e1")
                if self.cell_size >= 40 and (x, y) in self.env.walls:
                    self.canvas.create_text(x1 + self.cell_size / 2, y1 + self.cell_size / 2, text="W", fill="white", font=("Arial", 8, "bold"))

        for fx, fy in self.env.food_positions:
            offset = self.cell_size * 0.25
            x1 = fx * self.cell_size + offset
            y1 = (self.env.height - 1 - fy) * self.cell_size + offset
            self.canvas.create_oval(x1, y1, x1 + self.cell_size * 0.5, y1 + self.cell_size * 0.5, fill="#f59e0b", outline="#d97706")

        for ox, oy in self.env.opponents:
            offset = self.cell_size * 0.2
            x1 = ox * self.cell_size + offset
            y1 = (self.env.height - 1 - oy) * self.cell_size + offset
            self.canvas.create_rectangle(x1, y1, x1 + self.cell_size * 0.6, y1 + self.cell_size * 0.6, fill="#990000", outline="#7a0000")
                                         
        for tx, ty in self.env.toxic_traps:
            offset = self.cell_size * 0.25
            x1 = tx * self.cell_size + offset
            y1 = (self.env.height - 1 - ty) * self.cell_size + offset
            self.canvas.create_polygon(
                x1 + self.cell_size * 0.25, y1,
                x1, y1 + self.cell_size * 0.5,
                x1 + self.cell_size * 0.5, y1 + self.cell_size * 0.5,
                fill="#9333ea", outline="#7e22ce"
            )

        ax, ay = self.env.agent_pos
        offset = self.cell_size * 0.15
        x1 = ax * self.cell_size + offset
        y1 = (self.env.height - 1 - ay) * self.cell_size + offset
        self.canvas.create_oval(x1, y1, x1 + self.cell_size * 0.7, y1 + self.cell_size * 0.7, fill="#000066", outline="#1e3a8a")

    def run_loop(self):
        self.btn.config(state="disabled")
        
        # Using the Simple Reflex Agent!
        agent = ModelBasedAgent()

        def step():
            if not self.env.is_done():
                percept = self.env.get_percept()
                action = agent.sense_and_act(percept)
                self.env.execute_action(action)

                self.draw_grid()
                self.label.config(text=f"Score: {self.env.score} | Steps: {self.env.steps} | Action: {action}")
                self.root.after(250, step)
            else:
                end_text = f"Collision! Game Over! Final Score: {self.env.score}" if self.env.collision else f"Finished! Final Score: {self.env.score}"
                self.label.config(text=end_text)
                self.btn.config(state="normal")

        step()

if __name__ == "__main__":
    root = tk.Tk()
    app = GridGameGUI(root, width=12, height=12, num_food=15, num_opponents=0)
    root.mainloop()