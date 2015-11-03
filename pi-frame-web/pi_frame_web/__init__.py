"""
The flask application package.
"""

from flask import Flask

app = Flask(__name__)

import pi_frame_web.views