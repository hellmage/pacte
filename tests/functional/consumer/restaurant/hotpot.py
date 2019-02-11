# Copyright (c) 2018 App Annie Inc. All rights reserved.
import requests


def hotpot():
    response = requests.get('http://chicken-farm/buy-chicken?n=1000')
    return 'buy 1k chicken: %s' % response.text
