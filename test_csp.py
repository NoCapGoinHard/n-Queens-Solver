from src.csp_solver import CSPSolver, CSPConfig

def run_test():
    N = 8
    print(f"=== TEST CSP SOLVER (N={N}) ===\n")

    test_cases = [
        ("Pairwise Diagonal", CSPConfig(encoding="pairwise_diagonal")),
        ("AllDiff Diagonals", CSPConfig(encoding="alldiff_diagonals"))
    ]

    for name, config in test_cases:
        print(f"Testing mode: {name}")
        
        try:
            # Istanziamo il solver con la config specifica
            solver = CSPSolver(N, config=config)
            solution = solver.solve()
            metrics = solver.metrics

            if solution:
                print(f"  SUCCESS! Solution: {solution}")
                print(f"  Metrics:")
                print(f"  Time: {metrics['time_taken']:.6f} seconds")
                print(f"  Variables: {metrics.get('variables_count')}") 
                print(f"  Constraints: {metrics.get('constraints_count')}")
                print(f"  Solver Calls: {metrics.get('solver_calls')}")
            else:
                print("!!FAILURE!!: No solution found.")
        
        except Exception as e:
            print(f"!!!!CRITICAL ERROR!!!!: {e}")
        
        print("-" * 40)

if __name__ == "__main__":
    run_test()