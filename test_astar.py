from src.nqueens import NQueensProblem
from astar_solver import AStarSolver

def run_test():
    
    N = 8
    problem = NQueensProblem(N)
    
    solver = AStarSolver(problem, heuristic_code="1")
    
    solution = solver.solve()
    
    if solution:
        print("\n SOLUTION FOUND!")
        print(f"State Tuple: {solution}")
        
        conflicts = problem.count_conflicts(solution)
        print(f"Final Conflicts Check: {conflicts} (Should be 0)")
        assert conflicts == 0
        assert len(solution) == N
        
        print("\n METRICS:")
        print(f"  - Time: {solver.metrics['time_taken']:.5f} sec")
        print(f"  - Nodes Expanded: {solver.metrics['nodes_expanded']}")
        print(f"  - Nodes Generated: {solver.metrics['nodes_generated']}")
        print(f"  - Max Memory: {solver.metrics['max_memory']}")
        print(f"  - Branching Factor: {solver.metrics['branching_factor']:.2f}")
        
    else:
        print("\n NO SOLUTION FOUND (Something is wrong)")

if __name__ == "__main__":
    run_test()