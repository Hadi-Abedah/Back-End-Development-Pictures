from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for dic in data:
        if dic["id"] == id:
            return jsonify(dic)
    return jsonify({"error": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################

@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()
    if not picture:
        return jsonify({"error": "Request body must be JSON"}), 400
    
    if any(dic['id'] == picture['id'] for dic in data):
        return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

    data.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.get_json()
    if not picture:
        return jsonify({"error": "Request body must be JSON"}), 400

    pic_id = id
    for dic in data:
        if dic["id"] == pic_id:
            dic.update(picture)
            return jsonify(dic), 200
    
    return jsonify({"error": "Picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pic_id = id
    for dic in data:
        if dic["id"] == pic_id:
            data.remove(dic)
            return jsonify({"message": "Picture deleted"}), 204
    return jsonify({"message": "Picture not found"}), 404
