pyCANON
=======

|License| |Documentation Status| |Pipeline Status|

pyCANON is a Python library and CLI to assess the values of the parameters
associated with the most common privacy-preserving techniques via anonymization.

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

   import pandas as pd
   from pycanon import anonymity, report

   FILE_NAME = "adult.csv"
   QI = ["age", "education", "occupation", "relationship", "sex", "native-country"]
   SA = ["salary-class"]
   DATA = pd.read_csv(FILE_NAME)

   # Calculate k for k-anonymity:
   k = anonymity.k_anonymity(DATA, QI)

   # Print the anonymity report:
   report.print_report(DATA, QI, SA)

Description
-----------

pyCANON allows to check if the following privacy-preserving techniques
are verified and the value of the parameters associated with each of
them.

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

More information can be found in this `paper <https://www.nature.com/articles/s41597-022-01894-2>`__.


Citation
-----------
If you are using pyCANON you can cite it as follows:: 

   @article{sainzpardo2022pycanon,
      title={A Python library to check the level of anonymity of a dataset},
      author={S{\'a}inz-Pardo D{\'\i}az, Judith and L{\'o}pez Garc{\'\i}a, {\'A}lvaro},
      journal={Scientific Data},
      volume={9},
      number={1},
      pages={785},
      year={2022},
      publisher={Nature Publishing Group UK London}}

.. |License| image:: https://img.shields.io/badge/License-Apache_2.0-blue.svg
   :target: https://gitlab.ifca.es/sainzj/check-anonymity/-/blob/main/LICENSE
.. |Documentation Status| image:: https://readthedocs.org/projects/pycanon/badge/?version=latest
   :target: https://pycanon.readthedocs.io/en/latest/?badge=latest
.. |Pipeline Status| image:: https://gitlab.ifca.es/privacy-security/pycanon/badges/main/pipeline.svg
   :target: https://gitlab.ifca.es/privacy-security/pycanon/-/pipelines
