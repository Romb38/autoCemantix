import argparse
from src.configLoader import load_config
from src.CemantixSolver import CemantixSolver
from src.initialFiltering import filter_model_from_config

def main():
    parser = argparse.ArgumentParser(description="Cemantix solver and model initializer")
    parser.add_argument("command", choices=["solve", "init"], help="Command to run: solve or init")
    args = parser.parse_args()

    cfg = load_config()

    if args.command == "init":
        print("Initializing and filtering the dictionary/model...")
        filter_model_from_config(cfg)
        print("Initialization done.")
    elif args.command == "solve":
        solver = CemantixSolver(cfg)
        result = solver.solve()
        if result:
            print(result[0])

if __name__ == "__main__":
    main()

