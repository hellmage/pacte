# Copyright (c) 2018 App Annie Inc. All rights reserved.
from flask import Flask

app = Flask(__name__)


@app.route('/buy-chicken')
def buy_chicken():
    return 'success'
