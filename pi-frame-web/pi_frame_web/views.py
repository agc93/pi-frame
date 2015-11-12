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
settings = JsonReader("settings.json")
mount_points = dict([('media', """/media/media/Pictures/K/Dam/IMG_0142.JPG"""), ('home', """/media/media/Pictures/K/Home/IMG_8142.JPG""")])
run_command = 'fbi'
launch_args = ['-t', '25', '-a', '-u']
	
@app.route('/mounts')
def mounts():
	"""Renders the home page, with a list of all polls."""
	p = subprocess.Popen(['findmnt', '-o', 'SOURCE,SIZE,USE%,TARGET', '-t', 'nfs4,ext2,ext4'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	"""out,err = p.communicate()"""
	out = p.stdout.readlines()
	L = out
	return render_template(
		'index.html',
		title='Mount Points',
		year=datetime.now().year,
		mounts = L
	)
	
	
@app.route('/status')
def status():
	# Attempts to get status of slideshow
	p = subprocess.Popen(['pidof', run_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out,err = p.communicate()
	if out != None and out != "":
		out = out.rstrip('\n')
		s = subprocess.Popen(['ps', '-p', out], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		detail = s.stdout.readlines()
		if len(detail) == 1:
			return render_template(
				'error.html',
				message = "Process state unknown",
				output = "The process appears to be running, but we cannot get any further details",
				error = "pidof returned " + out + " but ps failed to find the process",
				path = "unknown",
				code = "?"
				)
		else:
			status = detail[1].rsplit()
			return render_template(
				'status.html',
				pid = out,
				console = status[1],
				time = status[2],
				process = status[3]
				)
	else:
		return render_template(
			'error.html',
			message = 'Process not running!',
			output = 'It appears the process is not running :( Try launching it again from the home page',
			error = 'pidof did not return a valid ID',
			path = "unknown",
			code = "?"
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
	full_args = buildArgs(launchPath)
	#raise
	p = subprocess.Popen(full_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	time.sleep(1)
	p.poll()
	if p.returncode != None:
		out,err = p.communicate()
		return render_template(
			'error.html',
			message = "Error launching process",
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

def buildArgs(launchPath):
	params = settings.read()
	launchPath = launchPath + "*"
	launch_args = []
	launch_args.append(run_command)
	launch_args.append('-t')
	params["time"]
	launch_args.append('a')
	launch_args.append('-u')
	launch_args.append(launchPath)
	return launch_args
