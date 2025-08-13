"""CLI entry point for llm_canvas.

Provides command-line interface for starting the local server.
"""

from __future__ import annotations

import argparse
import sys

from ._server import start_local_server


def main() -> None:  # pragma: no cover - CLI utility
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="LLM Canvas - Visualize LLM conversations as a navigable canvas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  llm-canvas server                    # Start local server on default port 8000
  llm-canvas server --port 3000       # Start local server on port 3000
  llm-canvas server --log-level debug # Start with debug logging
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Server subcommand
    server_parser = subparsers.add_parser("server", help="Start the local LLM Canvas server")
    server_parser.add_argument("--host", default="127.0.0.1", help="Host to serve on (default: 127.0.0.1)")
    server_parser.add_argument("--port", type=int, default=8000, help="Port to serve on (default: 8000)")
    server_parser.add_argument(
        "--log-level", default="info", choices=["debug", "info", "warning", "error"], help="Set logging level (default: info)"
    )

    args = parser.parse_args()

    if args.command == "server":
        start_local_server(host=args.host, port=args.port, log_level=args.log_level)
    elif args.command is None:
        # Default to server if no subcommand provided
        print("No command specified. Starting local server...")
        print("Use 'llm-canvas server --help' for more options.")
        start_local_server()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
