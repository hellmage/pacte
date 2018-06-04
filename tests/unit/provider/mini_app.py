# Copyright (c) 2017 App Annie Inc. All rights reserved.
import simplejson as json

from flask import Flask, request
from mock import MagicMock

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/json', methods=['GET', 'POST'])
def hello_json():
    if request.method == 'GET':
        key = request.args.get('key', 'sample_key')
        val = request.args.get('val', 'sample_val')
    else:
        data = json.loads(request.get_data())
        key = 'length'
        val = len(data)
    return json.dumps({key: val}), {'Content-Type': 'application/json'}


@app.route('/headers')
def hello_headers():
    assert request.headers.get('X-Pacte-Test') == 'bingo'
    return 'bingo', {'X-Pacte-Test': 'pango'}
