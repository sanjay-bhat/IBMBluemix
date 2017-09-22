"""
This script runs the IBMBlumixCloudComputing application using a development server.
"""

from os import environ
import flask
from IBMBlumixCloudComputing.views import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = '5000'
    #app.debug = True
    #app.run()
    app.add(HOST, PORT)
