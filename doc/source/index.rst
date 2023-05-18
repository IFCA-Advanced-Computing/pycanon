pyCANON: A Python library to check the level of anonymity of a dataset
======================================================================

pyCANON is a `Python`_ library which allows the user to know the anonymity
level of a dataset based on a set of quasi-identifiers (QI), and a set of
sensitive attributes. To do so, it provides a set of functions to compute the
anonymity level of a dataset by means of the following techniques:

* k-anonymity.
* (:math:`\alpha`,k)-anonymity.
* :math:`\ell`-diversity.
* Entropy :math:`\ell`-diversity.
* Recursive (c, :math:`\ell`)-diversity.
* t-closeness.
* Basic :math:`\beta`-likeness.
* Enhanced :math:`\beta`-likeness.
* :math:`\delta`-disclosure privacy.

.. _Python: https://www.python.org

User documentation
******************

.. toctree::
   :maxdepth: 4

   intro
   modules
   notes_warnings
   notes_utility

License
***********************

pyCANON is licensed under Apache License Version 2.0 (http://www.apache.org/licenses/)


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
