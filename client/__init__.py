import boto3
import json
import logging
import os

from flask import Flask
from flask_cors import CORS, cross_origin
from flask.ext.assets import Environment, Bundle


app = None
assets = None
db = None


def create_app():
    global app
    global assets
    global db

    app = Flask(__name__)

    app.config.from_object('config.dev')

    assets = Environment(app)
    register_keys()
    register_scss()
    db = register_db(app)

    CORS(app)

    return app

def register_db(app):
    boto_session = boto3.session.Session(aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])
    db = boto_session.resource('dynamodb',region_name='us-west-2')
    return db

def register_keys():
    os.environ['SECRET_KEY'] = app.config['STRIPE_SECRET_KEY']
    os.environ['PUBLISHABLE_KEY'] = app.config['STRIPE_PUBLISHABLE_KEY']

def register_scss():
    assets.url = app.static_url_path
    with open(app.config['SCSS_CONFIG_FILE']) as f:
        bundle_set = json.loads(f.read())
        output_folder = bundle_set['output_folder']
        depends = bundle_set['depends']
        for bundle_name, instructions in bundle_set['rules'].iteritems():
            bundle = Bundle(*instructions['inputs'],
                            output=output_folder + instructions['output'],
                            depends=depends,
                            filters='scss')
            assets.register(bundle_name, bundle)
