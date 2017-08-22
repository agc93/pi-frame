from flask import request, jsonify

from pi_frame_web import *
from pi_frame_web.file_read import *

reader = JsonReader("locations.json")


@app.route('/locations', methods=['POST'])
def add_location():
    name = request.form['name']
    location = request.form['location']
    mounts = reader.read()
    mounts.update({name: location})
    reader.write(mounts)
    return jsonify(mounts)


@app.route('/locations', methods=['DELETE'])
def delete_location():
    mounts = reader.read()
    name = request.form['name']
    del mounts[name]
    reader.write(mounts)
    return jsonify(mounts)


@app.route('/locations', methods=['GET'])
def get_locations():
    mounts = reader.read()
    return jsonify(**mounts)
