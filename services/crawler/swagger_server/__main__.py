#!/usr/bin/env python3

from conanci.config import app, db
from swagger_server import encoder
import os.path

swagger_api = os.path.join(os.path.dirname(__file__), 'swagger', 'swagger.yaml')


def main():
    app.add_api(swagger_api, arguments={'title': 'Conan CI Linux Agent'}, pythonic_params=True)
    app.app.json_encoder = encoder.JSONEncoder
    db.create_all()
    app.run(port=8080)

if __name__ == '__main__':
    main()
