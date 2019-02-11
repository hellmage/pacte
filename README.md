# Pacte

[![Build Status](https://travis-ci.org/luyun-aa/pacte.svg?branch=master)](https://travis-ci.org/luyun-aa/pacte)

This is an AppAnnie implementation of [Pact](pact.io). For now, we have
only implemented pact specification version 1.

`pacte` is a consumer driven contract testing library that allows mocking
of responses in the consumer codebase, and verification of the
interaction in the provider codebase.

`pacte` is based on [requests](https://github.com/kennethreitz/requests),
[requests-mock](https://github.com/jamielennox/requests-mock) and
[flask](https://github.com/pallets/flask). We assume that you, as a
consumer, is using the `requests` lib to make HTTP request. And as a
provider, you are developing your service using `flask`.

## Installation

```
pip install pacte
```

## Consumer Tests

Consumer test cases are just normal `unittest.TestCase`. `pacte` provides
a contract factory to initiate a contract and add interactions.

For example, you have some client side code like this:

```python
# tests/functional/consumer/restaurant/hotpot.py

def hotpot():
    response = requests.get('http://chicken-farm/buy-chicken?n=1000')
    return 'buy 1k chicken: %s' % response.text
```

The consumer side contract test case will look like this:

```python
# tests/functional/consumer/restaurant/test_http.py

class HTTPTest(unittest.TestCase):

    def test_http(self):
        contract = contract_factory.register('chicken-farm', 'HotPot')
        contract.given("10k-healthy-chickens").upon_receiving("one-thousand-buy-request").with_request(
            'GET', '/buy-chicken', query='n=1000'
        ).will_respond_with(200, body='success')
        with MockServices(MockAPI(contract, scheme='http', domain='chicken-farm')):
            result = hotpot()
            self.assertEqual('buy 1k chicken: success', result)
```

- `contract_factory`: a global factory to instantiate a `Contract` object.
- `contract`: it represent a contract, which is a collection of interactions
between the consumer and provider
  - `given`: the **state** clause, corresponds to a state class on provider
  side
  - `up_receiving`: the **description** clause, will be used as test case
  class name on provider side
  - `with_request`: details of the http request, including method, path,
  query, headers, body
  - `will_respond_with`: details of the http response, including status,
  headers, body
- `MockAPI`: mocker of interactions in a contract
- `MockServices`: mocker of one or more APIs

### How to run

`pacte` provides a wrapper of `nose` to run the consumer side contract
tests:

```
$ pact-consumer --help
Usage: pact-consumer [OPTIONS]

Options:
  --pact TEXT      Path to the directory to save contract files. It will be
                   created if not exists. Defaults to ".pact"
  --contract TEXT  Path to the consumer contract tests. Defaults to
                   "tests/contract/consumer"
  --help           Show this message and exit.
```

By default, `pact-consumer` will search for consumer side test cases in
`tests/contract/consumer` directory. Contract file in JSON format in the
`.pact` directory.

## Provider Tests

Provider is primarily responsible for preparing state classes. A valid
state class must meet the following requirements:

- must be a subclass of `unittest.TestCase`
- file name must start with `state_`
- class name must start with `State`
- must have a class attribute `state`

Suppose you have a microservice:

```python
# tests/functional/provider/app.py

app = Flask(__name__)


@app.route('/buy-chicken')
def buy_chicken():
    return 'success'
```

A state class will look like:

```python
# tests/functional/provider/states/state_healthy_chickens.py

class StateHealthyChickens(unittest.TestCase):
    state = '10k-healthy-chickens'

    def setUp(self):
        pass

    def tearDown(self):
        pass
```

Please beware that no test method in state class is necessary. Interactions
defined in the contract provided by consumer side will be transformed into
test method automatically. The purpose of state class is to implement data
preparation in the `setUp` and `tearDown` method. You can insert records
into database, or mock downstream microservices, or do anything necessary
to meet the request and response from consumer side contract.

### How to run

`pacte` also provides a wrapper of `nose` to run the provider side contract
tests:

```
$ pact-provider --help
Usage: pact-provider [OPTIONS] CONTRACT

Options:
  --statedir TEXT  Directory for state preparation scripts. Defaults to
                   "tests/contract/provider"
  --app TEXT       The Flask application instance. Defaults to "app.app"
  --help           Show this message and exit.
```

The `pact-provider` command will load all state classes from the `statedir`
and dynamically generate test cases from the provided contract. The generated
test cases will also be run by `nose`.

## Development

Run tests:

```shell
make test
```
