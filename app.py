#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__version__ = '1.0.0'
__license__ = 'MIT'
__author__ = 'Josh Welchez'
__email__ = 'jshwelz09@gmail.com'


from flask import Flask, jsonify
from globals import db, config
from commands import register_commands
from flask_cors import CORS, cross_origin
import routes


def init_app():
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "*"}})
    app.config['CORS_HEADERS'] = 'Content-Type'

    db.connect()
    app.config['SECRET_KEY'] = config.SECRET

    @app.route('/')
    def hello_world():
        return 'Hotels Api'

    routes.initialize_routes(app)
    register_commands(app)
    return app


app = init_app()


if __name__ == '__main__':
    app.run()
