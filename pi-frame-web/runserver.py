"""
This script runs the pi_frame_web application using a development server.
"""

from os import environ
from pi_frame_web import app
from flask_debugtoolbar import DebugToolbarExtension
import sys

#import ptvsd
#ptvsd.enable_attach(secret='ptvsd', address = ('localhost', 12345))
#ptvsd.wait_for_attach(timeout = 10)

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '0.0.0.0')
    print HOST
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    debugMode = environ.get('APP_DEBUG', False)
    if __debug__:
        app.debug = True
        app.config['SECRET_KEY'] = '0123456789'
        toolbar = DebugToolbarExtension(app)
    app.run(HOST, PORT)
