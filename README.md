# Optimove

[![Build Status](https://travis-ci.org/nicolasramy/optimove.svg?branch=master)](https://travis-ci.org/nicolasramy/optimove)
[![Coverage Status](https://coveralls.io/repos/github/nicolasramy/optimove/badge.svg?branch=master)](https://coveralls.io/github/nicolasramy/optimove?branch=master)

**This library allows you to quickly and easily use the Optimove Web API v3 via Python**

## Installation

### Requirements

* [requests](docs.python-requests.org/en/latest/index.html)

see ```requirements.txt``` for more details

### Install package

```
python setup.py install
```

## Quick start

### Create a new client

```python
from optimove.client import Client
client = Client('username', 'password')
````

Or

```python
from optimove.client import Client
client = Client()
client.general.login('username', 'password')
```

## Test

Tests are available in ```tests/``` folder, before to run them, you should install [responses](https://github.com/getsentry/responses).
This package is used to bind the HTTP call to Optimove API.

The fixture used for the tests are from the documentation provided by Optimove

### Requirements

* [responses](https://github.com/getsentry/responses)

```
python setup.py test
```

## Usage

## Roadmap

## How to contribute

## Troubleshooting

## About
