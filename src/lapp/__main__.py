import argparse
from .api.app import create_app

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run the Flask application')
    parser.add_argument(
        '--env',
        choices=['dev', 'test', 'prod'],
        default='dev',
        help='Environment to run in (default: dev)'
    )
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host to run on (default: 127.0.0.1)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port to run on (default: 5000)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode (overrides environment setting)'
    )
    return parser.parse_args()


def main():
    args = parse_args()
    
    # Create app with specified environment
    app = create_app(config_name=args.env)
    
    # Override debug if specified
    if args.debug:
        app.config['DEBUG'] = True
    
    print(f"🚀 Starting Flask server in {args.env} mode")
    print(f"📍 Running on http://{args.host}:{args.port}")
    
    # Run the app
    app.run(
        host=args.host,
        port=args.port,
        debug=app.config.get('DEBUG', False)
    )

if __name__ == '__main__':
    main()