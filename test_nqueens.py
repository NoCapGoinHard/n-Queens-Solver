from src.nqueens import NQueensProblem

prob = NQueensProblem(4)

initial = prob.get_initial_state()
print(f"Initial: {initial}, EXPECTED '()'")

succs = prob.get_successors(initial)
print(f"First step successors (EXPECTED: 4): {len(succs)}")
print(f"First successor: {succs[0]}") # EXPECTED: the placement print with "(0, 0)", (0,), 1

bad_state = (0, 0) 
print(f"Conflicts in (0,0): {prob.count_conflicts(bad_state)} EXPECTED 1") 

diag_state = (0, 1)
print(f"Conflicts in (0,1): {prob.count_conflicts(diag_state)} EXPECTED 1") 

good_state = (1, 3)
print(f"Conflicts in (1,3): {prob.count_conflicts(good_state)} EXPECTED 0") 