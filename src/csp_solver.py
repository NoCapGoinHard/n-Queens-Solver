import time
from constraint import Problem, AllDifferentConstraint

class CSPSolver:
    """
    solver for N-Queens by reduction to CSP
    leveraging python-constraint library
    """

    def __init__(self, n):
        self.n = n
        self.metrics = {
            "time_taken": 0.0,
            "nodes": 0,
            "solution": None
        }

    def solve(self):
        start_time = time.perf_counter()

        problem = Problem()

        cols = range(self.n)
        rows = range(self.n)
        problem.addVariables(cols, rows)

        problem.addConstraint(AllDifferentConstraint())

        for c1 in cols:
            for c2 in cols:
                if c1 < c2:
                    def diagonal_conflict(r1, r2, c1=c1, c2=c2):
                        diff_row = abs(r1 - r2)
                        diff_col = abs(c1 - c2)
                        return diff_row != diff_col
                    problem.addConstraint(diagonal_conflict, (c1, c2))

        solution_dict = problem.getSolution()

        end_time = time.perf_counter()
        self.metrics["time_taken"] = end_time - start_time

        if solution_dict:
            solution_tuple = tuple(solution_dict[i] for i in range(self.n))
            self.metrics["solution"] = solution_tuple
            return solution_tuple
        else:
            return None