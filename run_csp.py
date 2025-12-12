import time
import csv
import os
from src.csp_solver import CSPSolver, CSPConfig

STARTING_N = 4
MAX_N = 50
TIMEOUT_LIMIT_SECONDS = 300
REPORT_DIR = "experiments"
CSV_CSP = "csp_results.csv"

def run_csp_experiments():
    os.makedirs(REPORT_DIR, exist_ok=True)
    path_csp = os.path.join(REPORT_DIR, CSV_CSP)

    with open(path_csp, mode="w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "ALG",
            "N",
            "ENCODING",
            "TIME_TAKEN",
            "VARIABLES",
            "CONSTRAINTS",
            "SOLVER_CALLS",
            "SOLUTIONS_FOUND"
        ])
    
    active_status = {
        "pairwise_diagonal": True,
        "alldiff_diagonals": True,
    }

    print("PROGRESS: STARTING CSP EXPERIMENTS\n")

    for n in range(STARTING_N, MAX_N + 1):
        # Se tutti gli algoritmi sono disattivi, stop totale
        if not any(active_status.values()):
            print("PROGRESS: ALL CSP ENCODINGS HAVE REACHED THE TIME LIMIT.\n EXPERIMENT ENDED.\n")
            break

        print(f"\nPROGRESS: N = {n}")

        encodings_to_run = ["pairwise_diagonal", "alldiff_diagonals"]
        
        for encoding in encodings_to_run:

            if not active_status[encoding]: #SKIP IF DISABLED!
                continue

            print(f"PROGRESS: solving {encoding} encoding", end="", flush=True)

            try:
                config = CSPConfig(encoding=encoding, max_solutions_to_collect=1)
                solver = CSPSolver(n, config=config)

                solution = solver.solve()
                metrics = solver.metrics
                time_taken = metrics["time_taken"]

                vars_count = metrics.get('variables_count', 'N/A')
                constr_count = metrics.get('constraints_count', 'N/A')

                print(f"\n    DONE IN {time_taken:.4f} sec. | Vars: {vars_count} | Constr: {constr_count}")
                save_row_csp(path_csp, "CSP", n, metrics)

                if time_taken >= TIMEOUT_LIMIT_SECONDS:
                    active_status[encoding] = False
                    print(f"    [!] PROGRESS: TIME LIMIT REACHED FOR [{encoding}]. DISABLING IT.")

            except Exception as e:
                print(f"\n !!ERROR!! CSP {encoding} failed: {e}")
                active_status[encoding] = False

    print("\n[END] CSP EXPERIMENT HAS CONCLUDED")

def save_row_csp(path, alg, n, metrics):
    with open(path, mode="a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            alg,
            n,
            metrics.get("encoding", "unknown"),
            f"{metrics['time_taken']:.8f}",
            metrics.get("variables_count", 0),
            metrics.get("constraints_count", 0),
            metrics.get("solver_calls", 0),
            metrics.get("solutions_found", 0)
        ])

if __name__ == "__main__":
    run_csp_experiments()