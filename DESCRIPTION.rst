Genie Libs Telemetry Component
==============================

Genie Telemetry is a testbed Health Status Monitoring Tool. It is a package
within pyATS.

pyATS is an end-to-end testing ecosystem, specializing in data-driven and
reusable testing, and engineered to be suitable for Agile, rapid development
iterations. Extensible by design, pyATS enables developers start with small,
simple and linear test cases, and scale towards large, complex and asynchronous
test suites.

Genie was initially developed internally in Cisco, and is now available to the
general public starting early 2018 through `Cisco DevNet`_. Visit the Genie
home page at

    https://developer.cisco.com/site/pyats/

.. _Cisco DevNet: https://developer.cisco.com/


Parser Package
------------

This is a sub-component of Genie that parse the device output into structure
datastructure.

Requirements
------------

Genie currently supports Python 3.4+ on Linux & Mac systems. Windows platforms
are not yet supported.

Quick Start
-----------

.. code-block:: console
 
    # install pyats as a whole
    $ pip install pyats

    # install genie as a whole
    $ pip install genie

    # to upgrade this package manually
    $ pip install --upgrade genie.libs.telemetry

    # to install alpha/beta versions, add --pre
    $ pip install --pre genie.libs.telemetry


For more information on setting up your Python development environment,
such as creating virtual environment and installing ``pip`` on your system, 
please refer to `Virtual Environment and Packages`_ in Python tutorials.

.. _Virtual Environment and Packages: https://docs.python.org/3/tutorial/venv.html
