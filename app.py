from flask import Flask, request, jsonify
from service import PackingService
from models import Schema

import json

app = Flask(__name__)

@app.route("/")
def hello():
    return 'Hello world!'

@app.route("/<name>")
def hello_name(name):
    return "Hello " + name

@app.route("/packing", methods=["GET"])
def list_packing():
    return jsonify(PackingService().list())

@app.route("/packing", methods=["POST"])
def create_packing():
    return jsonify(PackingService().create(request.get_json()))

@app.route("/packing/<item_id>", methods=["PUT"])
def update_item():
    return jsonify(PackingService().update(item_id, request.get_json()))

@app.route("/packing/<item_id>", methods=["DELETE"])
def delete_item():
    return jsonify(PackingService().delete(item_id))


if __name__=='__main__':
    Schema()
    app.run(debug=True)