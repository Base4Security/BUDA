import argparse
from .app import main as start
from .version import __version__

def main():
    """
    Function to parse command-line arguments and start the BUDA framework.

    Command-line arguments:
        --host, -H: Host to run the server on (default: '127.0.0.1')
        --port, -p: Port to run the server on (default: 9875)
        --verbosity, -v: Verbosity level ('TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR') (default: 'INFO')
    """
    parser = argparse.ArgumentParser(description='BUDA CLI')
    parser.add_argument('--version', action='version', version=__version__, help="show program's version number and exit")    
    parser.add_argument('--host', '-H', default='127.0.0.1', help='Host to run the server on')
    parser.add_argument('--port', '-p', type=int, default=9875, help='Port to run the server on')
    parser.add_argument('--verbosity', '-v', choices=['TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR'], default='INFO', help='Verbosity level')

    args = parser.parse_args()

    # Start the server
    start(host=args.host, port=args.port, verbosity=args.verbosity)

if __name__ == '__main__':
    main()