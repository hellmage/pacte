# Copyright (c) 2018 App Annie Inc. All rights reserved.
import requests


def mcdonald():
    response = requests.get('http://www.chicken-farm.com/buy-chicken?n=1000')
    return 'buy 1k chicken: %s' % response.text
