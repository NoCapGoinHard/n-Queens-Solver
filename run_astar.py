import time
import csv
import os
from src.nqueens import NQueensProblem
from src.astar_solver import AStarSolver

STARTING_N = 4
MAX_N = 50
TIMEOUT_LIMIT_SECONDS = 300
REPORT_DIR = "experiments"
CSV_ASTAR = "astar_results.csv"

def run_astar_experiments():
    os.makedirs(REPORT_DIR, exist_ok=True)
    path_astar = os.path.join(REPORT_DIR, CSV_ASTAR)

    with open(path_astar, mode="w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "ALG",
            "HEURISTIC",
            "N",
            "TIME_TAKEN",
            "NODES_EXPANDED",
            "NODES_GENERATED",
            "MAX_MEMORY",
            "SOLUTION_COST",
            "BRANCHING_FACTOR",
        ])

    # Status tracking for A* heuristics
    active_status = {
        "A*_h0": False,
        "A*_h1": True,
        "A*_h2": True
    }

    print("PROGRESS: STARTING A* EXPERIMENTS\n")

    for n in range(STARTING_N, MAX_N + 1):
        if not any(active_status.values()):
            print("         ALL A* HEURISTICS HAVE REACHED THE TIME LIMIT.\n EXPERIMENT ENDED.\n")
            break
        
        print(f"\nPROGRESS: N = {n}")

        #### A* BLOCK ###########
        for h_code, h_name in [("0", "h0"), ("1", "h1"), ("2", "h2")]:
            alg_key = f"A*_{h_name}"

            if active_status[alg_key]:
                print(f"PROGRESS: solving with A*, heuristic: {h_name}", end="", flush=True)

                try:
                    problem = NQueensProblem(n)
                    solver = AStarSolver(problem, heuristic_code=h_code)
                    solver.solve()

                    metrics = solver.metrics
                    time_taken = metrics["time_taken"]

                    print(f"\n  PROGRESS: DONE IN {time_taken:.12f} seconds. | NODES EXPANDED: {metrics['nodes_expanded']}")

                    save_row_astar(path_astar, "A*", h_name, n, metrics)

                    if time_taken >= TIMEOUT_LIMIT_SECONDS:
                        active_status[alg_key] = False
                        print(f"[!] PROGRESS: A* with {h_name} reached the fixed time limit. stop exploirng N's with this heuristics.")
                    
                except Exception as e:
                    print(f"ERROR: {e}")
                    active_status[alg_key] = False

            else:
                pass

    print("[END] PROGRESS: ALL A* EXPERIMENTS HAVE BEEN DONE.\n")

def save_row_astar(path, alg, heuristic, n, metrics):
    with open(path, mode="a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            alg,
            heuristic,
            n,
            f"{metrics['time_taken']:.12f}",
            metrics["nodes_expanded"],
            metrics["nodes_generated"],
            metrics["max_memory"],
            metrics["solution_cost"],
            f"{metrics['branching_factor']:.12f}",
        ])

if __name__ == "__main__":
    run_astar_experiments()