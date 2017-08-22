from flask import render_template, redirect, request, jsonify

from pi_frame_web import *
from os import *
from pi_frame_web.file_read import *

reader = JsonReader("locations.json")

@app.route('/locations', methods=['POST'])
def addLocation():
    name = request.form['name']
    location = request.form['location']
    mounts = reader.read()
    mounts.update({name: location})
    reader.write(mounts)
    return jsonify(mounts)

@app.route('/locations', methods=['DELETE'])
def deleteLocation():
    mounts = reader.read()
    name = request.form['name']
    del mounts[name]
    reader.write(mounts)
    return jsonify(mounts)

@app.route('/locations', methods=['GET'])
def getLocations():
    mounts = reader.read()
    return jsonify(**mounts)
