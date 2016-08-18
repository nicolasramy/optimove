Optimove
========

|PyPI version| |Build Status| |Coverage Status|

**This library allows you to quickly and easily use the Optimove Web API
v3 via Python**

Installation
------------

Requirements
~~~~~~~~~~~~

-  `requests <docs.python-requests.org/en/latest/index.html>`__

see ``requirements.txt`` for more details

Install package
~~~~~~~~~~~~~~~

::

    python setup.py install

Quick start
-----------

Create a new client
~~~~~~~~~~~~~~~~~~~

.. code:: python

    from optimove.client import Client
    client = Client('username', 'password')

Or

.. code:: python

    from optimove.client import Client
    client = Client()
    client.general.login('username', 'password')

Test
----

Tests are available in ``tests/`` folder, before to run them, you should
install `responses <https://github.com/getsentry/responses>`__. This
package is used to bind the HTTP call to Optimove API.

The fixture used for the tests are from the documentation provided by
Optimove

Requirements
~~~~~~~~~~~~

-  `responses <https://github.com/getsentry/responses>`__

::

    python setup.py test

Usage
-----

Roadmap
-------

How to contribute
-----------------

Troubleshooting
---------------

About
-----

.. |PyPI version| image:: https://badge.fury.io/py/optimove.svg
   :target: https://badge.fury.io/py/optimove
.. |Build Status| image:: https://travis-ci.org/nicolasramy/optimove.svg?branch=master
   :target: https://travis-ci.org/nicolasramy/optimove
.. |Coverage Status| image:: https://coveralls.io/repos/github/nicolasramy/optimove/badge.svg?branch=master
   :target: https://coveralls.io/github/nicolasramy/optimove?branch=master

