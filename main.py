from flask_server import FlaskServer
import sys

if __name__ == '__main__':
    server = FlaskServer()
    if len(sys.argv) < 2:
        print ('The application should gets argument with the address of redis server')
    else:
        server.init_redis(sys.argv[1])
        server.run_server()
