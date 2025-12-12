import time
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, List, Any, Iterable

from constraint import Problem, AllDifferentConstraint


@dataclass(frozen=True)
class CSPConfig:
    """
    Configuration for the CSP reduction.
    """
    encoding: str = "pairwise_diagonal"
    max_solutions_to_collect: int = 1  # Collect up to this many solutions (1 = first solution only)


class CSPSolver:
    """
    CSP solver for N-Queens by reduction to CSP (python-constraint).

    Variables:
      - One variable per column (0..n-1)
      - Value is the row index (0..n-1)

    Supported encodings:
      - "pairwise_diagonal": O(n^2) binary constraints for diagonals
      - "alldiff_diagonals": auxiliary diagonal-id variables + AllDifferent on diagonals
    """

    def __init__(self, n: int, config: Optional[CSPConfig] = None):

        self.n = n
        self.config = config or CSPConfig()

        self.metrics: Dict[str, Any] = {
            # Timing
            "time_taken": 0.0,

            # Problem infos
            "n": n,
            "encoding": self.config.encoding,

            # CSP structure metric
            "variables_count": 0,
            "constraints_count": 0,
            "domain_size_mean": float(n),

            "row_variables_count": n,
            "aux_variables_count": 0,

            "solver_calls": 0,
            "solutions_found": 0,

            "solution": None,
            "solutions_collected": [], # only when specificed more than 1
        }

    def solve(self) -> Optional[Tuple[int, ...]]:
        start_time = time.perf_counter()

        problem = Problem()

        cols = list(range(self.n))
        rows = list(range(self.n))
        problem.addVariables(cols, rows)

        #all queens must be in different ROWS
        problem.addConstraint(AllDifferentConstraint(), cols)

        #DIAGONAL constraints
        if self.config.encoding == "pairwise_diagonal":
            self.metrics["diagonal_constraints_mode"] = "binary_pairwise"
            self._add_pairwise_diagonal_constraints(problem, cols)
        elif self.config.encoding == "alldiff_diagonals":
            self.metrics["diagonal_constraints_mode"] = "alldiff_aux"
            self._add_alldiff_diagonal_constraints(problem, cols)
        else:
            raise ValueError(f"Unknown encoding: {self.config.encoding}")

        self._fill_structure_metrics(problem)

        solutions = self._collect_solutions(problem, cols)

        end_time = time.perf_counter()
        self.metrics["time_taken"] = end_time - start_time

        if not solutions:
            self.metrics["solution"] = None
            self.metrics["solutions_collected"] = []
            return None

        first_solution = solutions[0] #the first one is the main one
        self.metrics["solutions_collected"] = solutions
        self.metrics["solution"] = first_solution

        return first_solution


    def _add_pairwise_diagonal_constraints(self, problem: Problem, cols: List[int]) -> None:
        """
        Pairwise diagonal constraints encoding:
        For each pair of columns (c1, c2), enforce (r1 - r2) != (c1 - c2) (absolute values)
        complexity: O(n^2) BINARY constraints.
        """
        for c1 in cols:
            for c2 in range(c1 + 1, self.n):
                # Capture c1/c2 at definition time via default args (important in Python closures)
                def no_diagonal_conflict(r1: int, r2: int, c1=c1, c2=c2) -> bool:
                    return abs(r1 - r2) != abs(c1 - c2)

                problem.addConstraint(no_diagonal_conflict, (c1, c2))

    def _add_alldiff_diagonal_constraints(self, problem: Problem, cols: List[int]) -> None:
        """
        For each column c with row r:
          d1 = r - c  (main diagonal id)
          d2 = r + c  (anti diagonal id)
        Enforce:
          AllDifferent(d1_0..d1_{n-1})
          AllDifferent(d2_0..d2_{n-1})

        This introduces:
          - 2n auxiliary variables (d1_c, d2_c)
          - 2n linking constraints
          - 2 AllDifferent constraints
        """
        d1_vars = [f"d1_{c}" for c in cols]  # r - c
        d2_vars = [f"d2_{c}" for c in cols]  # r + c

        # Domains:
        # r in [0, n-1], c in [0, n-1]
        # d1 in [-(n-1), +(n-1)]
        # d2 in [0, 2(n-1)]
        d1_domain = list(range(-(self.n - 1), self.n))
        d2_domain = list(range(0, 2 * (self.n - 1) + 1))

        problem.addVariables(d1_vars, d1_domain)
        problem.addVariables(d2_vars, d2_domain)

        # Track auxiliary variable count (we control this)
        self.metrics["aux_variables_count"] = 2 * self.n

        for c in cols:
            row_var = c
            d1 = f"d1_{c}"
            d2 = f"d2_{c}"

            def link_d1(r: int, d: int, c=c) -> bool:
                return d == r - c

            def link_d2(r: int, d: int, c=c) -> bool:
                return d == r + c

            problem.addConstraint(link_d1, (row_var, d1))
            problem.addConstraint(link_d2, (row_var, d2))

        problem.addConstraint(AllDifferentConstraint(), d1_vars)
        problem.addConstraint(AllDifferentConstraint(), d2_vars)

    # ---------------------------------------------------------------------
    # Solving + metrics utilities
    # ---------------------------------------------------------------------

    def _collect_solutions(self, problem: Problem, cols: List[int]) -> List[Tuple[int, ...]]:
        """
        Collect up to max_solutions_to_collect variable (settable in config) solutions using an iterator.

        This avoids getSolutions() which can return way too much things for larger scaling parameter (namely N).
        Updates metrics:
          - solver_calls
          - solutions_found
        """
        self.metrics["solver_calls"] += 1

        it = problem.getSolutionIter()
        solutions: List[Tuple[int, ...]] = []

        for sol_dict in it:
            self.metrics["solutions_found"] += 1
            sol_tuple = tuple(sol_dict[c] for c in cols)
            solutions.append(sol_tuple)

            if len(solutions) >= self.config.max_solutions_to_collect:
                break

        return solutions

    def _fill_structure_metrics(self, problem: Problem) -> None:
        """
        Best-effort extraction of CSP size metrics.
        """
        vars_count = None
        constraints_count = None

        try:
            if hasattr(problem, "_variables"):
                vars_count = len(problem._variables)
            if hasattr(problem, "_constraints"):
                constraints_count = len(problem._constraints)
        except Exception:
            pass

        self.metrics["variables_count"] = vars_count if vars_count is not None else self.n
        self.metrics["constraints_count"] = constraints_count if constraints_count is not None else "N/A"
