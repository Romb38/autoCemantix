import argparse
from src.configLoader import load_config
from src.CemantixSolver import CemantixSolver
from src.initialFiltering import filter_model_from_config
from src.generateStatsGraph import create_graph_stats

def main():
    parser = argparse.ArgumentParser(description="Cemantix solver and model initializer")
    parser.add_argument("command", choices=["solve", "init", "generate-stat-graph"], help="Command to run: solve, generate-stat-graph or init")
    args = parser.parse_args()

    cfg = load_config()

    if args.command == "init":
        filter_model_from_config(cfg)
    elif args.command == "solve":
        solver = CemantixSolver(cfg)
        result = solver.solve()
    elif args.command == "generate-stat-graph":
        create_graph_stats(cfg)


if __name__ == "__main__":
    main()
