# N-Queens Solver: Search (A*) vs. CSP

This repository contains the homework project for the **Artificial Intelligence** course.
The goal is to solve the N-Queens problem using two different paradigms and compare their performance:

1.  **Informed Search:** A* Algorithm with two different heuristics.
2.  **Constraint Satisfaction (CSP):** Using `python-constraint` with two different encodings.

## Requirements

Ensure you have Python 3.x installed. The project relies on the following libraries:

python-constraint
matplotlib
pandas

It is recommended to create a virtual environment so to install packages in a confined portion of your machine (although 2/3 packages are the most commonly used for any purpose)
The easiest way to install them is to clone the repository and run:
```bash
python -m pip install -r requirements.txt
```

## Project Structure

The project is organized modularly to separate the algorithm logic, execution scripts, and result analysis.

* `src/`: Contains the core source code and main classes.
    * `nqueens.py`: Defines the `NQueensProblem` class, including state representation, transitions, and heuristic functions ($h_1, h_2$).
    * `astar_solver.py`: Manual implementation of the **A*** search algorithm. It handles the frontier (priority queue), cost calculation $f(n) = g(n) + h(n)$, and metric collection (nodes expanded, memory, branching factor).
    * `csp_solver.py`: Solver implementation based on **Constraint Satisfaction** (CSP) using the `python-constraint` library. It supports two distinct encodings (Pairwise and AllDiff with auxiliary variables) and tracks structural metrics (variables and constraints count).

* `experiments/`: Automatically generated output directory.
    * Contains raw data CSV files (`astar_results.csv`, `csp_results.csv`).
    * Contains the generated analysis plots (e.g., `plot_comparison_log.png`).

* `run_astar.py`: Main script to execute A* experiments. It iterates over increasing values of $N$ and different heuristics until the timeout is reached.
* `run_csp.py`: Main script to execute CSP experiments. It compares the two encodings (Pairwise vs AllDiff) as $N$ increases.
* `plot_results.py`: Data analysis script. It reads CSVs from the `experiments/` folder and generates comparative plots (log-scale execution time, search space analysis).
* `test_csp.py`: Sanity check to assess everything is ok.
* `test_astar.py`: Sanity check to assess everything is ok.
* `test_nqueens.py`: Sanity check to assess everything is ok.


## Recommended run sequence
To run, just open each file in vscode and press the icon to run
* `test_csp.py`
* `test_astar.py`
* `test_nqueens.py`
If everything is ok, proceed with the run of the solvers. They will automatically increase the scaling factor and treat the heuristics (A*) as a survival race. Feel free to adjust the constant variables at the top as you want.
* `run_astar.py`
* `run_csp.py`
+ `report_results.py`
