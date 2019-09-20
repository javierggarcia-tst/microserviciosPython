# encoding: utf-8
from flask_script import Manager
from waitress import serve

from place.app import create_app

app = create_app()

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8082)