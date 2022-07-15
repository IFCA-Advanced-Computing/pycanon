Getting started
###############

Using pyCANON is quite straighforward.

Install
***********************

We recommend using ``pip`` for installing *pycanon* inside a ``virtualenv``:

.. code-block:: console

   virtualenv .venv
   source .venv/bin/activate
   git clone https://gitlab.ifca.es/privacy-security/pycanon/
   pip install py.canon


Example usage
*************

You can use pyCANON through the command line or via its Python API.

Command line
------------

Example with the `adult dataset`_:

.. code-block:: console

   $ pycanon k-anonymity --qi age --qi education --qi occupation --qi relationship --qi sex --qi native-country adult.csv

   $ pycanon report --sa salary-class --qi age --qi education --qi occupation --qi relationship --qi sex --qi native-country adult.csv



Python API
----------

Example with the `adult dataset`_:

.. code-block:: python

    from pycanon import anonymity, report

    FILE_NAME = "adult.csv"
    QI = ["age", "education", "occupation", "relationship", "sex", "native-country"]
    SA = ["salary-class"]

    # Calculate k for k-anonymity:
    k = anonymity.k_anonymity(FILE_NAME, QI)

    # Print the anonymity report:
    report.print_report(FILE_NAME, QI, SA)


.. _adult dataset: https://archive.ics.uci.edu/ml/datasets/adult
