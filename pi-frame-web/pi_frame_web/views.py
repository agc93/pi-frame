﻿# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""

from datetime import datetime

from flask import render_template, redirect, request, jsonify

from pi_frame_web import app
from os import *
from os.path import isfile, join
import subprocess
import time
from pi_frame_web.file_read import *
from pi_frame_web.process_details import *
from pi_frame_web.location_details import *
import os
import signal

reader = JsonReader("locations.json")
settings = JsonReader("settings.json")
mount_points = dict([('media', """/media/media/Pictures/K/Dam/IMG_0142.JPG"""),
                     ('home', """/media/media/Pictures/K/Home/IMG_8142.JPG""")])
run_command = 'fbi'


@app.route('/mounts')
def mounts():
    """Renders the home page, with a list of all polls."""
    p = subprocess.Popen(['findmnt', '-o', 'SOURCE,SIZE,USE%,TARGET', '-t', 'nfs4,ext2,ext4'], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    """out,err = p.communicate()"""
    out = p.stdout.readlines()
    L = out
    return render_template(
        'index.html',
        title='Mount Points',
        year=datetime.now().year,
        mounts=L
    )


@app.route('/status')
def status():
    # Attempts to get status of slideshow
    p = subprocess.Popen(['pidof', run_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if out is not None and out != "":
        out = out.rstrip('\n')
        s = subprocess.Popen(['ps', '-p', out], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        detail = s.stdout.readlines()
        if len(detail) == 1:
            return render_template(
                'error.html',
                message="Process state unknown",
                output="The process appears to be running, but we cannot get any further details",
                error="pidof returned " + out + " but ps failed to find the process",
                path="unknown",
                code="?"
            )
        else:
            status = detail[1].rsplit()
            return render_template(
                'status.html',
                pid=out,
                console=status[1],
                time=status[2],
                process=status[3]
            )
    else:
        return render_template(
            'error.html',
            message='Process not running!',
            output='It appears the process is not running :( Try launching it again from the home page',
            error='pidof did not return a valid ID',
            path="unknown",
            code="?"
        )


@app.route('/')
@app.route('/home')
def launch():
    return render_template(
        'launch.html',
        locations=reader.read()
    )


@app.route('/create')
def input():
    return render_template('input.html')


@app.route('/list')
def list_albums():
    locations = reader.read()
    location_details = []
    for location in locations:
        try:
            files = get_files(locations[location])
        except:
            files = []
        album = LocationDetails(location, locations[location], len(files))
        location_details.append(album)
    # raise
    return render_template(
        'albums.html',
        albums=location_details
    )


@app.route('/start', methods=['GET', 'POST'])
@app.route('/start/<folder_path>', methods=['GET', 'POST'])
def start_get(folder_path=""):
    # folder_path = request.args.get('folder_path')

    if folder_path == "":
        # folder_path = request.form['folder_path']
        folder_path = request.args.get('folder_path')
    locations = reader.read()
    launch_path = locations[folder_path]
    return start_process(launch_path)


@app.route('/post', methods=['POST'])
def start_post():
    locations = reader.read()
    launch_path = locations[request.form['folderPath']]
    return start_process(launch_path)


@app.route('/stop', methods=['GET'])
def stop_running():
    kill_existing()
    return redirect('status')


def start_process(launch_path):
    # full_args = build_args()
    # raise
    kill_existing()
    try:
        dir_files = get_files(launch_path)
    except:
        return render_template(
            'error.html',
            message="Could not open directory " + launch_path,
            path=launch_path
        )
    files = dir_files + dir_files
    full_args = build_args() + files
    # raise
    p = subprocess.Popen(full_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)
    p.poll()
    if p.returncode is not None:
        out, err = p.communicate()
        return render_template(
            'error.html',
            message="Error launching process",
            path=launch_path,
            code=p.returncode,
            output=out,
            error=err)
    else:
        return render_template(
            'confirm.html',
            path=launch_path,
            code=p.returncode,
            year=datetime.now().minute
        )


def build_args():
    params = settings.read()
    launch_args = [run_command, '-t', params["time"], '-a', '-u', params["deviceArg"], params["device"]]
    return launch_args


def get_files(folder_path):
    files = [join(folder_path, f) for f in listdir(folder_path) if isfile(join(folder_path, f))]
    return files


def kill_existing():
    p = ProcessDetails(run_command)
    pids = p.get_PIDs()
    if pids is None:
        return
    else:
        for pid in pids:
            try:
                os.kill(int(pid), signal.SIGTERM)
            except ValueError:
                break
