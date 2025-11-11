from django.apps import AppConfig
import sys


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        # Only print URLs when running the development server
        if 'runserver' in sys.argv:
            # Get the default port or from command line
            # runserver can be: runserver, runserver 8000, runserver 0.0.0.0:8000
            port = '8000'
            host = '127.0.0.1'
            
            # Find runserver argument index
            try:
                runserver_idx = sys.argv.index('runserver')
                if len(sys.argv) > runserver_idx + 1:
                    addr = sys.argv[runserver_idx + 1]
                    if ':' in addr:
                        host, port = addr.split(':')
                    else:
                        port = addr
            except (ValueError, IndexError):
                pass
            
            base_url = f'http://{host}:{port}'
            
            print('\n' + '=' * 60)
            print('API Documentation:')
            print('=' * 60)
            print(f'Swagger UI is ready on: {base_url}/api/docs/swagger/')
            print(f'ReDoc is ready on: {base_url}/api/docs/redoc/')
            print('=' * 60 + '\n')
