import argparse
from src.configLoader import load_config
from src.CemantixSolver import CemantixSolver
from src.generateStatsGraph import create_graph_stats

def main():
    parser = argparse.ArgumentParser(description="Cemantix solver and model initializer")

    parser.add_argument(
        "--config", "-c",
        default="src/resources/config.ini",
        help="Path to the configuration file (default: src/resources/config.ini)"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    filtering_parser = subparsers.add_parser("filter", help="Filter the model. By default, use the local glossary with rules listed in README.md")
    filtering_parser.add_argument("-c", "--cemantix", action="store_true", help="Use Cemantix API to filter model instead of local rules. Use with caution as it can take a long time")
    filtering_parser.add_argument("-n", "--ntfy", action="store_true", help="Notify users using NTFY API when filtering ends. Must have NTFY configured in .env and curl installed")

    subparsers.add_parser("generate-stat-graph", help="Generate statistics graph")

    solve_parser = subparsers.add_parser("solve", help="Solve Cemantix")
    solve_parser.add_argument("-f", "--filtering", action="store_true", help="Enable filtering before solving")
    solve_parser.add_argument("-s", "--stats", action="store_true", help="Save solving statistics. Must have a statistics file defined in configuration")
    solve_parser.add_argument("-n", "--ntfy", action="store_true", help="Notify users using NTFY API with satistics. Must have NTFY configured in .env and curl installed")

    args = parser.parse_args()
    cfg = load_config(args.config)

    if args.command == "filter":
        solver = CemantixSolver(cfg)
        if args.cemantix:
            solver.cemantixFiltering(
                ntfy=args.ntfy
            )
        else:
            solver.localFiltering(
                ntfy=args.ntfy
            )
    elif args.command == "solve":
        solver = CemantixSolver(cfg)
        result = solver.solve(
            filtering=args.filtering,
            save_stats=args.stats,
            ntfy=args.ntfy
        )
    elif args.command == "generate-stat-graph":
        create_graph_stats(cfg)

if __name__ == "__main__":
    main()
