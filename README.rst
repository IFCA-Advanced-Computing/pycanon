pyCANON
=======

|made-with-python| |License| |Documentation Status|

pyCANON is a library and CLI to assess the values of the paramenters
associated with the most common privacy-preserving techniques.

**Authors:** Judith Sáinz-Pardo Díaz and Álvaro López García (IFCA - CSIC).

Installation
------------

We recommend to use Python3 with
`virtualenv <https://virtualenv.pypa.io/en/latest/>`__:

::

   virtualenv .venv -p python3
   source .venv/bin/activate

Then run the following command to install the library and all its
requirements:

::

   pip install pycanon

Documentation
-------------

The pyCANON documentation is hosted on `Read the
Docs <https://pycanon.readthedocs.io/>`__.

Getting started
---------------

Example using the `adult
dataset <https://archive.ics.uci.edu/ml/datasets/adult>`__:

.. code:: python

   from pycanon import anonymity, report

   FILE_NAME = "adult.csv"
   QI = ["age", "education", "occupation", "relationship", "sex", "native-country"]
   SA = ["salary-class"]

   # Calculate k for k-anonymity:
   k = anonymity.k_anonymity(FILE_NAME, QI)

   # Print the anonymity report:
   report.print_report(FILE_NAME, QI, SA)

Description
-----------

pyCANON allows to check if the following privacy-preserving techniques
are verified and the value of the parameters associated with each of
them:

+---------------------------+-----------------------------+------------+-----------------------------------------------------+
| Technique                 | pyCANON function            | Parameters | Notes                                               |
+===========================+=============================+============+=====================================================+
| k-anonymity               | ``k_anonymity``             | *k*: int   |                                                     |
+---------------------------+-----------------------------+------------+-----------------------------------------------------+
| (α, k)-anonymity          | ``alpha_k_anonymity``       | *α*: float |                                                     |
|                           |                             | *k*:int    |                                                     |
+---------------------------+-----------------------------+------------+-----------------------------------------------------+
| ℓ-diversity               | ``l_diversity``             | *ℓ*: int   |                                                     |
+---------------------------+-----------------------------+------------+-----------------------------------------------------+
| Entropy ℓ-diversity       | ``entropy_l_diversity``     | *ℓ*: int   |                                                     |
+---------------------------+-----------------------------+------------+-----------------------------------------------------+
| Recursive (c,ℓ)-diversity | ``recursive_c_l_diversity`` | *c*: int   | Not calculated if ℓ=1                               |
|                           |                             | *ℓ*: int   |                                                     |
+---------------------------+-----------------------------+------------+-----------------------------------------------------+
| Basic β-likeness          | ``basic_beta_likeness``     | *β*: float |                                                     |
+---------------------------+-----------------------------+------------+-----------------------------------------------------+
| Enhanced β-likeness       | ``enhanced_beta_likeness``  | *β*: float |                                                     |
+---------------------------+-----------------------------+------------+-----------------------------------------------------+
| t-closeness               | ``t_closeness``             | *t*: float | For numerical attributes the definition of the EMD  |
|                           |                             |            | (one-dimensional Earth Mover’s Distance) is used.   |
|                           |                             |            | For categorical attributes, the metric "Equal       |
|                           |                             |            | Distance" is used.                                  |
+---------------------------+-----------------------------+------------+-----------------------------------------------------+
| δ-disclosure privacy      | ``delta_disclosure``        | *δ*: float |                                                     |
+---------------------------+-----------------------------+------------+-----------------------------------------------------+


.. |made-with-python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
   :target: https://www.python.org/
.. |License| image:: https://img.shields.io/badge/License-Apache_2.0-blue.svg
   :target: https://gitlab.ifca.es/sainzj/check-anonymity/-/blob/main/LICENSE
.. |Documentation Status| image:: https://readthedocs.org/projects/pycanon/badge/?version=latest
   :target: https://pycanon.readthedocs.io/en/latest/?badge=latest
