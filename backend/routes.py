import json
import os

from flask import abort, jsonify, make_response, request, url_for  # noqa; F401

from . import app

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
    if data:
        return jsonify(data), 200
    return {"message": "Internal server error"}, 500
     
######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for d in data:
            if d['id'] == id:
                return jsonify(d), 200
            
        return {"message": "Not found"}, 404
    return {"message": "Internal server error"}, 500



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    try:
        picture = request.get_json()
        for d in data:
            if d['id'] == picture['id']:
                return {"Message": f"picture with id {picture['id']} already present"}, 302
        data.append(picture)
        return jsonify(picture), 201
    except Exception as e:
        return {"message": f"Internal Server Error: \n{e}"}, 500


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.get_json()
    if picture is None:
        return jsonify({"message": "Internal server error"})
    for d in data:
        if d["id"] == id:
            d.update(picture)  # Update the existing dictionary
            return jsonify(d), 200

    return jsonify({"error": "Picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for d in data:
        if d['id'] == id:
            data.remove(d)
            return make_response('', 204)
    return jsonify({"error": "Picture not found"}), 404
