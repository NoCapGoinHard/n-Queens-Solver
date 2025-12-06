import heapq
import time
from src.nqueens import HEURISTICS

class AStarSolver:
    """
    Manual implementation as requested by professors
    As planned, it has been made in a way one could apply it with whatever heuristic is wanted
    """

    def __init__(self, problem, heuristic_code="1"):
        """
        :param heuristic_name: switcher for heuristics (DEFINED IN nqueens.py)
        """
        self.problem = problem

        if heuristic_code not in HEURISTICS:
            raise ValueError(f"Wrong hueristic code")
        self.heuristic_func = HEURISTICS[heuristic_code]

        self.metrics = {
            "time_taken": 0.0,
            "nodes_expanded": 0,    
            "nodes_generated": 0,   
            "max_memory": 0,        
            "solution_cost": 0,
            "solution_depth": 0,
            "branching_factor": 0.0 
        }

    def solve(self):
        start_time = time.time()
        
        frontier = []
        tie_breaker = 0

        initial_state = self.problem.get_initial_state()
        h_start = self.heuristic_func(self.problem, initial_state)

        heapq.heappush(frontier, (h_start, tie_breaker, initial_state, 0))
        self.metrics["nodes_generated"] += 1

        explored = set()

        while frontier:
            current_memory = len(frontier) + len(explored)
            if current_memory > self.metrics["max_memory"]:
                self.metrics["max_memory"] = current_memory

            current_f, _, current_state, current_g = heapq.heappop(frontier)

            if current_state in explored:
                continue

            explored.add(current_state)
            self.metrics["nodes_expanded"] += 1

            if self.problem.is_goal(current_state):
                self._finalize_metrics(start_time, current_g, len(current_state))
                return current_state
            
            for action, neighbor, step_cost in self.problem.get_successors(current_state):
                if neighbor in explored:
                    continue

                new_g = current_g + step_cost
                h = self.heuristic_func(self.problem, neighbor)
                new_f = new_g + h

                tie_breaker += 1
                heapq.heappush(frontier, (new_f, tie_breaker, neighbor, new_g))
                self.metrics["nodes_generated"] += 1

        self._finalize_metrics(start_time, 0, 0)
        return None
    
    def _finalize_metrics(self, start_time, cost, depth):
        """
        saving info for report
        """
        end_time = time.time()
        self.metrics["time_taken"] = end_time - start_time
        self.metrics["solution_cost"] = cost
        self.metrics["solution_depth"] = depth

        if self.metrics["nodes_expanded"] > 0:
            self.metrics["branching_factor"] = self.metrics["nodes_generated"] / self.metrics["nodes_expanded"]
            