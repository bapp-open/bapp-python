# BAPP Python API Client

BAPP was built from the ground-up to be API-first. This means that we build out the API endpoints for all of our features, and the UI is simply a wrapper around these endpoints.

To interface with BAPP using Python, we've created a `bapp` client library.

> If you want to access the API directly, please refer to our [API Documentation](https://developer.bapp.ro)

## Installation

To install the `bapp` library, simply run the command:

`pip install bapp`

## Quickstart

Getting up and running with the Python library is quick and easy.

To start, simply create an account [Register page](https://app.bapp.ro/auth/register).

```python
from bapp import BappClient

bapp = BappClient(email='email', password='password')
```
or
```python
from bapp import BappClient

bapp = BappClient(token='token', dev=True)
```
Now you're ready to start using the API!
