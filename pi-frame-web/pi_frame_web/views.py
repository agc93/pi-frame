# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""

from datetime import datetime

from flask import render_template, redirect, request, jsonify

from pi_frame_web import app
from os import *
import subprocess
import time

mount_points = dict([('media', """/media/media/Pictures/K/Dam/IMG_0142.JPG"""), ('home', """/media/media/Pictures/K/Home/IMG_8142.JPG""")])
run_command = 'fbi'

@app.route('/locations', methods=['POST'])
def addLocation():
    name = request.form['name']
    location = request.form['location']
    mount_points.update({name: location})
    return jsonify(mount_points)

@app.route('/locations', methods=['DELETE'])
def deleteLocation():
    name = request.form['name']
    del mount_points[name]
    return jsonify(mount_points)

@app.route('/locations', methods=['GET'])
def getLocations():
    return jsonify(**mount_points)

@app.route('/home')
def home():
    """Renders the home page, with a list of all polls."""
    p = subprocess.Popen(['findmnt', '-o', 'SOURCE,SIZE,USE%,TARGET', '-t', 'nfs4,ext2,ext4'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    """out,err = p.communicate()"""
    out = p.stdout.readlines()
    L = out[0]
    return render_template(
        'index.html',
        title='Mount Points',
        year=datetime.now().year,
        mounts = L
    )

@app.route('/')
@app.route('/input')
def input():
    return render_template('input.html')

@app.route('/start/<folderPath>')
def start(folderPath):
    launchPath=mount_points[folderPath]
    p = subprocess.Popen([run_command, launchPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)
    p.poll()
    if p.returncode != None:
        out,err = p.communicate()
        return render_template(
            'error.html',
            code = p.returncode,
            output = out,
            error = err)
    else:
        return render_template(
            'confirm.html',
            path=launchPath,
            code = p.returncode,
            year=datetime.now().minute
            )
