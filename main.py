from src.configLoader import load_config
from src.CemantixSolver import CemantixSolver

cfg = load_config()
solver = CemantixSolver(cfg)
result = solver.solve()
if result:
    print(result[0])