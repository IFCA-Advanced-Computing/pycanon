Getting started
###############

Using pyCANON is quite straighforward.

Install
***********************

We recommend using ``pip`` for installing pyCANON inside a ``virtualenv``:

.. code-block:: console

    virtualenv .venv
    source .venv/bin/activate
    pip install pycanon

Installing with support for PDF reports: If you want to generate PDF reports with
`ReportLab <https://docs.reportlab.com/>`_ you need to use the following install
command:

   .. code-block:: console

    pip install pycanon[PDF]

If you want to use the latest development version, you can use:

.. code-block:: console

   virtualenv .venv
   source .venv/bin/activate
   git clone https://gitlab.ifca.es/privacy-security/pycanon/
   pip install pycanon


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
    DATA = pd.read_csv(FILE_NAME)

    # Calculate k for k-anonymity:
    k = anonymity.k_anonymity(DATA, QI)

    # Print the anonymity report:
    report.print_report(DATA, QI, SA)


.. _adult dataset: https://archive.ics.uci.edu/ml/datasets/adult
