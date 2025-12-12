import time
import csv
import os
from src.csp_solver import CSPSolver

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
            "TIME_TAKEN",
        ])
    
    # Status tracking for CSP
    active_status = {
        "CSP": True
    }

    print("PROGRESS: STARTING CSP EXPERIMENTS\n")

    for n in range(STARTING_N, MAX_N + 1):
        if not active_status["CSP"]:
            print("         CSP HAS REACHED THE TIME LIMIT.\n EXPERIMENT ENDED.\n")
            break
        
        print(f"\nPROGRESS: N = {n}")

        ### CSP BLOCK ###########
        if active_status["CSP"]:
            print(f"PROGRESS: solving now with CSP", end="", flush=True)
            try:
                solver = CSPSolver(n)

                solution = solver.solve()
                time_taken = solver.metrics["time_taken"]

                print(f"\n    PROGRESS: DONE IN {time_taken:.12f} seconds.")

                save_row_csp(path_csp, "CSP", n, time_taken)

                if time_taken >= TIMEOUT_LIMIT_SECONDS:
                    active_status["CSP"] = False
                    print(f"[!]PROGRESS: CSP reached time limit. stop exploring N's with CSP.")

            except Exception as e:
                print(f"ERROR: {e}")
                active_status["CSP"] = False

    print("[END] PROGRESS: ALL CSP EXPERIMENTS HAVE BEEN DONE.\n")

def save_row_csp(path, alg, n, time_taken):
    with open(path, mode="a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            alg,
            n,
            f"{time_taken:.8f}",
        ])

if __name__ == "__main__":
    run_csp_experiments()