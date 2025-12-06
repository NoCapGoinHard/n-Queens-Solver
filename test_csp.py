from src.csp_solver import CSPSolver

def run_test():
    N = 64
    print("N = ", N)
    solver = CSPSolver(N)
    solution = solver.solve()
    
    if solution:
        print(f"Solution Found: {solution}")
        print(f"Time: {solver.metrics['time_taken']:.6f} seconds")
    else:
        print("No solution found.")

if __name__ == "__main__":
    run_test()