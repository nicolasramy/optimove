Optimove
========

|PyPI version| |Travis CI| |Coveralls|

This library allows you to quickly and easily use the Optimove Web API
via Python based on `Optimove
documentation <https://docs.optimove.com/api-usage-guide/>`__

Installation
------------

From Pypi
~~~~~~~~~

.. code:: bash

        pip install optimove

From source
~~~~~~~~~~~

.. code:: bash

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

Tests are available in ``tests/`` folder.

The fixture used for the tests are from the documentation provided by
Optimove.

.. code:: bash

        python setup.py test

Usage
-----

Roadmap
-------

Missing features
~~~~~~~~~~~~~~~~

-  [ ] Add missing pagination parameters / Refacto pagination parameters
   (maybe with a decorator)
-  [ ] Test pagination
-  [ ] Better authentication management
-  [ ] Auto-reconnect as soon as possible (based on expire value)
-  [ ] Use custom exceptions
-  [ ] Prepare compatibility with Python 3.4+

New API functions
~~~~~~~~~~~~~~~~~

-  [ ]
   [GetCustomerOneTimeActionsByCampaign](http://docs.optimove.com/api-usage-guide/#GetCustomerOneTimeActionsByCampaign)
   – Returns a list of customers and the details associated with a
   particular one-time campaign (i.e., via a manually-imported customer
   list)
-  [ ]
   [SendTransactionalMail](http://docs.optimove.com/api-usage-guide/#SendTransactionalMail)
   – Sends a transactional email to a list of recipients
-  [ ]
   [GetTransactionalTemplateMetrics](http://docs.optimove.com/api-usage-guide/#GetTransactionalTemplateMetrics)
   – Returns post-execution metrics for a specific transactional mail
   template over time
-  [ ]
   [GetTransactionalUserMetrics](http://docs.optimove.com/api-usage-guide/#GetTransactionalUserMetrics)
   – Returns post-execution transactional email metrics for a specific
   recipient
-  [ ]
   [GetCustomerProductsByCampaign](http://docs.optimove.com/api-usage-guide/#GetCustomerProductDetailsByCampaign)
   - Returns an array of customer IDs and recommended Product IDs for
   each customer targeted by a particular product recommendation
   campaign
-  [ ]
   [GetCustomerProductDetailsByDate](http://docs.optimove.com/api-usage-guide/#GetCustomerProductDetailsByDate)
   – Returns an array of customer IDs and recommended Product IDs for
   each customer targeted by any product recommendation campaign on a
   particular date
-  [ ]
   [GetCampaignInteractionCustomers](http://docs.optimove.com/api-usage-guide/#GetCampaignInteractionCustomers)
   – Returns an array of Customer IDs and the Campaign ID and Template
   ID for each customer who performed a particular interaction with a
   campaign that was delivered on a particular date via a particular
   channel

How to contribute
-----------------

Troubleshooting
---------------

For any issue please `create a new
issue <https://github.com/nicolasramy/optimove/issues/new>`__

About
-----

.. |PyPI version| image:: https://badge.fury.io/py/optimove.svg
   :target: https://badge.fury.io/py/optimove
.. |Travis CI| image:: https://travis-ci.org/nicolasramy/optimove.svg?branch=master
   :target: https://travis-ci.org/nicolasramy/optimove
.. |Coveralls| image:: https://coveralls.io/repos/github/nicolasramy/optimove/badge.svg?branch=master
   :target: https://coveralls.io/github/nicolasramy/optimove?branch=master
