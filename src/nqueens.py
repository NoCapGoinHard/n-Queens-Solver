class NQueensProblem:
    """
    Models the well known N-Queens problem to be solved in an algorithm-agnostic way
    Given the process pipeline for any solver (always easier to work with numbers),
    the chessboard has not been defined as the real one (with letters on cells),
    ensuring no need for parsing and intermediate steps that may significantly increase the computational performances

    STATE REPR.
        a tuple of integers, specifying where the queen is in terms of tuple index, and tuple value.
        the tuple length corresponds to the number of queens to position onto the chessboard
        - the index (i) is the COLUMN of interest
        - the value (v) is the ROW (of the i-th column) where the queen is meant to be placed
        EXAMPLE: (1, 4, 4) means: queen in C0, R1, queen in C1, R4, queen in C2, R4
    """

    def __init__(self, n):
        """        
        :param n: the number of queens
        """
        self.n = n

    def get_initial_state(self):
        return ()
    
    def is_goal(self, state):
        """
        GOAL DEFINITION:
        A -> all the queens are placed well
        B -> no conflicts
        """
        return len(state) == self.n and self.count_conflicts(state) == 0
    
    def get_successors(self, state):
        """
        Generates next states by adding a queen in the next free column
        Returns a tuple list (ACTION, NEW STATE, COST)
        """
        current_col = len(state)

        #if all the columns have been filled, no successors (return empty tuple)
        if current_col >= self.n:
            return []

        successors = []
        for row in range(self.n):
            new_state = state + (row,) #immutable tuple
            action = f"Place at ({current_col}, {row})"
            cost = 1
            successors.append((action, new_state, cost))
        
        return successors
    
    def count_conflicts(self, state):
        """
        counts how many couples of queens can eat each other
        """
        conflicts = 0
        num_queens = len(state)

        for i in range(num_queens):
            for j in range(i+1, num_queens):
                row_i = state[i]
                row_j = state[j]

                if row_i == row_j:
                    conflicts += 1
                    continue
                    
                delta_row = abs(row_i - row_j)
                delta_col = abs(i - j)

                if delta_row == delta_col:
                    conflicts += 1

        return conflicts
    
def heuristic0_null(problem, state):
    """
    in order to demonstrate what happens without heuristics
    """
    return 0

def heuristic1_conflicts(problem, state):
    """
    relies on conflicts
    """
    return problem.count_conflicts(state)

def heuristic2_aggressive(problem, state):
    """
    penalizes conflicts in heavier way
    even with only one conflict, makes the state very expensive
    in order to discourage its exploartion
    """
    conflicts = problem.count_conflicts(state)
    return conflicts * 10

#MODULAR SWITCH CASE

HEURISTICS = {
    "0": heuristic0_null,
    "1": heuristic1_conflicts,
    "2": heuristic2_aggressive
}