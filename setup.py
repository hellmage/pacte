# Copyright (c) 2017 App Annie Inc. All rights reserved.
import re
from setuptools import setup

VERSION = None
with open('./pacte/__init__.py') as f:
    for line in f:
        line = line.strip()
        match = re.search(r'^VERSION *= *.(\d+\.\d+\.\d+).$', line)
        if match:
            VERSION = match.group(1)
            break
assert VERSION

setup(
    name='pacte',
    packages=['pacte', 'pacte.utils'],
    version=VERSION,
    description='Consumer driven contract testing library.',
    author='Luyun Xie',
    author_email='luyun@appannie.com',
    url='http://github.com/luyun-aa/pacte',
    keywords=['testing', 'pact'],
    classifiers=[],
    install_requires=[
        'flask>=0.12',
        'requests-mock==1.4.0',
        'requests==2.18.1',
        'simplejson==3.6.5',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'pact-provider=pacte.pact:provider',
            'pact-consumer=pacte.pact:consumer',
        ]
    },
)
