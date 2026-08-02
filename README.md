# IT3012 - Intelligent Agents Lab 01

This repository contains the completed implementation for the IT3012 Intelligent Agents assignment. The project simulates a multi-agent grid environment where a primary agent must navigate a board to collect food while avoiding hazards and moving opponents.

## 🚀 Features Implemented

### 1. Intelligent Agents (`agent.py`)
* **Simple Reflex Agent:** Reacts purely to immediate sensory percepts (e.g., eating food if present, turning away from walls) without any memory of past states.
* **Model-Based Agent:** Maintains an internal state (memory) of its previous actions to avoid getting stuck in infinite loops when trapped in corners.
* **Search Agent:** Implements Breadth-First Search (BFS) for offline planning, allowing the agent to find the optimal (shortest) path to a goal while navigating around static obstacles.

### 2. Environment Modifications (`visual_grid_game.py`)
* **Toxic Traps (New Hazard):** Added hidden toxic traps to the environment to enforce partial observability. 
* **Expanded Sensors:** The agent's percept dictionary now includes a `smells_toxin` sensor to detect traps dynamically.
* **Visual Rendering:** Traps are rendered on the Tkinter GUI as custom purple triangles.

---

## 📂 File Structure
* `agent.py`: Contains the logic and decision-making algorithms for the different agent types.
* `visual_grid_game.py`: Contains the environment logic (`VisualGridHuntGame`) and the visual Tkinter wrapper (`GridGameGUI`).
* `test_suite.py`: The autograder unit tests to verify agent functionality and BFS pathfinding.

---

## 🛠️ How to Run & Test

### 1. Running the Agent Autograder (Unit Tests)
To verify that the logic for all agents is functioning correctly, run the test suite from your terminal:
```bash
python test_suite.py