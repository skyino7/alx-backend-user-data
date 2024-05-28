#!usr/bin/env python3

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome():
    """Return a welcome message"""
    return jsonify({"message": "Bienvenue"})
