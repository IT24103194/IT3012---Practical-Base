# IT3012 - Intelligent Agents: Lab 02

This repository contains the completed implementation for the IT3012 Intelligent Agents assignment. The project simulates a partially observable grid environment where a primary agent must navigate a board to collect food while avoiding hazards and moving opponents.

## 🚀 Features Implemented

### 1. Agent Architectures (`agent.py`)
* **Simple Reflex Agent:** Reacts purely to immediate sensory percepts using strict Condition-Action (IF-THEN) rules without any memory of past states. (Note: Prone to infinite loops under partial observability).
* **Model-Based Agent:** Maintains an internal state (memory) using a `stuck_counter` to track its previous actions. By utilizing a Transition and Sensor model, it successfully breaks out of infinite loops when trapped in corners.
* **Search Agent:** Implements Breadth-First Search (BFS) for offline planning, allowing the agent to find the optimal (shortest) path to a goal while navigating around static obstacles.

### 2. Environment Modifications (`visual_grid_game.py`)
* **Partial Observability Constraints:** The environment limits the agent to local Boolean sensors rather than global map knowledge.
* **Toxic Traps (New Hazard):** Added hidden toxic traps to the environment to enforce and test partial observability survival. 
* **Expanded Sensors:** The agent's percept dictionary now includes a `smells_toxin` sensor to detect traps dynamically.
* **Visual Rendering:** Traps are rendered on the Tkinter GUI as custom purple triangles.

---

## 📂 File Structure
* `agent.py`: Contains the logic, internal states, and decision-making algorithms for the different agent architectures.
* `visual_grid_game.py`: Contains the environment logic (`VisualGridHuntGame`) and the visual Tkinter wrapper (`GridGameGUI`).
* `test_suite.py`: The autograder unit tests to verify agent functionality and BFS pathfinding.

---

## 🛠️ How to Run & Test

### 1. Running the Agent Autograder (Unit Tests)
To verify that the logic for all agents is functioning correctly, run the test suite from your terminal:

```bash
python test_suite.py