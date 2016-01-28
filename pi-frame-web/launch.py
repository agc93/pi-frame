"""
This script runs the pi_frame_web application using a development server.
"""

from os import environ
from pi_frame_web import app
import sys

if __name__ == '__main__':
    app.run()
