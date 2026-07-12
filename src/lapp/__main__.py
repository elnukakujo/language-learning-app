import argparse
import os
from .api.app import create_app

def parse_args():
    """Parse command line arguments. Each flag falls back to an env var, then a default."""
    parser = argparse.ArgumentParser(description='Run the Flask application')
    parser.add_argument(
        '--env',
        choices=['dev', 'test', 'prod'],
        default=os.environ.get('LAPP_ENV', 'dev'),
        help='Environment to run in (default: dev, env: LAPP_ENV)'
    )
    parser.add_argument(
        '--host',
        default=os.environ.get('LAPP_HOST', '127.0.0.1'),
        help='Host to run on (default: 127.0.0.1, env: LAPP_HOST)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=int(os.environ.get('LAPP_PORT', 5000)),
        help='Port to run on (default: 5000, env: LAPP_PORT)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        default=os.environ.get('LAPP_DEBUG', '').lower() in ('1', 'true', 'yes'),
        help='Enable debug mode (overrides environment setting, env: LAPP_DEBUG)'
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