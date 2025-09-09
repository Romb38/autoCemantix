import argparse
from src.configLoader import load_config
from src.CemantixSolver import CemantixSolver

def main():
    parser = argparse.ArgumentParser(description="Cemantix solver and model initializer")

    parser.add_argument(
        "--config", "-c",
        default="src/resources/config.ini",
        help="Path to the configuration file (default: src/resources/config.ini)"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    solve_parser = subparsers.add_parser("solve", help="Solve Cemantix using local methods. It is currently the fastest one")
    solve_parser.add_argument("-n", "--ntfy", action="store_true", help="Notify users using NTFY API with satistics. Must have NTFY configured in .env and curl installed")

    args = parser.parse_args()
    cfg = load_config(args.config)


    if args.command == "solve":
        solver = CemantixSolver(cfg)
        result = solver.solve(
            ntfy=args.ntfy
        )

if __name__ == "__main__":
    main()
