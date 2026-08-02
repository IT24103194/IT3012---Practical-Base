import random
from collections import deque

class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""
    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        return random.choice(self.actions_pool)


class SimpleReflexAgent:
    """
    Practical 1: Acts strictly on the current percept.
    Has no memory of past actions or states.
    """
    def sense_and_act(self, percept: dict) -> str:
        # Scenario A: Food is present
        if percept.get('food_here'):
            return 'Eat'
        
        # Scenario B: Wall is ahead
        if percept.get('wall_ahead'):
            # Must return a valid movement action to turn away
            return random.choice(['Left', 'Right', 'Down', 'Up'])
            
        # Default action
        return 'Up'


class ModelBasedAgent:
    """
    Practical 2: Maintains internal state (memory) to avoid getting stuck 
    in infinite loops when facing the same percept multiple times.
    """
    def __init__(self):
        self.last_action = None

    def sense_and_act(self, percept: dict) -> str:
        if percept.get('wall_ahead'):
            possible_actions = ['Left', 'Right', 'Down', 'Up']
            
            # Use internal state to NOT repeat the exact same failure
            if self.last_action in possible_actions:
                possible_actions.remove(self.last_action)
                
            chosen_action = random.choice(possible_actions)
            self.last_action = chosen_action
            return chosen_action
            
        return 'Up'


class SearchAgent:
    """
    Practical 3: Uses offline planning (Breadth-First Search) to find 
    the optimal path to a goal before taking any actions.
    """
    def bfs_search(self, start_pos: tuple, goal_pos: tuple, walls: list, grid_size: tuple) -> list:
        width, height = grid_size
        walls_set = set(walls)
        
        # Queue stores tuples of: (current_position, path_taken_to_get_here)
        queue = deque([(start_pos, [])])
        visited = {start_pos}
        
        moves = {
            'Up': (0, 1),
            'Down': (0, -1),
            'Left': (-1, 0),
            'Right': (1, 0)
        }
        
        while queue:
            (x, y), path = queue.popleft()
            
            # Check if we reached the goal
            if (x, y) == goal_pos:
                return path
            
            # Explore neighbors
            for action_name, (dx, dy) in moves.items():
                nx, ny = x + dx, y + dy
                next_pos = (nx, ny)
                
                # Check grid boundaries
                if 0 <= nx < width and 0 <= ny < height:
                    # Check for collisions and previously visited nodes
                    if next_pos not in walls_set and next_pos not in visited:
                        visited.add(next_pos)
                        queue.append((next_pos, path + [action_name]))
                        
        # Goal is unreachable (boxed in by walls)
        return []