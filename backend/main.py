"""
Main script for managing backend, tests, and database.
"""

import argparse
import subprocess
import uvicorn

def run_pytest():
    """
    Run pytest for unit tests.
    """
    print("Running tests with pytest...")
    result = subprocess.run(['pytest', '-v'], capture_output=True, text=True)

    if result.returncode == 0:
        print("All tests passed!")
    else:
        print("Tests failed. Please check the output.")
    
    print(result.stdout)
    return result.returncode

def _run_server(host="0.0.0.0", port=5000):
    """
    Start the FastAPI development server.
    Default: host = 0.0.0.0, port = 5000.
    """
    print(f"Starting FastAPI server at {host}:{port}")
    uvicorn.run('rule_engine.main:app', host=host, port=port, reload=True)

def parse_arguments():
    """
    Parse command-line arguments for script execution.
    """
    parser = argparse.ArgumentParser(
        description="Manage the backend, run tests, or start a local server.",
        allow_abbrev=False
    )

    parser.add_argument(
        '--tests', 
        action='store_true', 
        help='Run pytest for unit tests'
    )
    parser.add_argument(
        '--dev', 
        action='store_true', 
        help='Run the FastAPI development server'
    )
    parser.add_argument(
        '--host', 
        type=str, 
        default="0.0.0.0", 
        help='Specify the host for the FastAPI server (default: 0.0.0.0)'
    )
    parser.add_argument(
        '--port', 
        type=int, 
        default=5000, 
        help='Specify the port for the FastAPI server (default: 5000)'
    )

    return parser.parse_args()

def main():
    """
    Entry point for the application. 
    Execute tasks based on provided command-line arguments.
    """
    args = parse_arguments()

    if args.tests:
        returncode = run_pytest()
        if returncode != 0:
            print("Some tests failed.")
    elif args.dev:
        _run_server(host=args.host, port=args.port)
    else:
        print("Invalid command. Use '--help' for usage information.")

if __name__ == "__main__":
    main()

