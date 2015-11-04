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
from file_read import *

reader = JsonReader("locations.json")
mount_points = dict([('media', """/media/media/Pictures/K/Dam/IMG_0142.JPG"""), ('home', """/media/media/Pictures/K/Home/IMG_8142.JPG""")])
run_command = 'fbi'
    
@app.route('/mounts')
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

@app.route('/home')
def launch():
    return render_template(
        'launch.html',
        locations = reader.read()
        )

@app.route('/')
@app.route('/input')
def input():
    return render_template('input.html')

@app.route('/start')
@app.route('/start/<folderPath>', methods = ['GET', 'POST'])
def startGet(folderPath = ""):
    #folderPath = request.args.get('folderPath')
    
    if folderPath == "":
        #folderPath = request.form['folderPath']
        folderPath = request.args.get('folderPath')
    locations = reader.read()
    launchPath=locations[folderPath]
    return startProcess(launchPath)
    
@app.route('/post', methods = ['POST'])
def startPost():
    locations = reader.read()
    launchPath = locations[request.form['folderPath']]
    return startProcess(launchPath)
    
def startProcess(launchPath):
    #raise
    p = subprocess.Popen([run_command, launchPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)
    p.poll()
    if p.returncode != None:
        out,err = p.communicate()
        return render_template(
            'error.html',
            path = launchPath,
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
