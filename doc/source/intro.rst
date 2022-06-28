Whats's pycanon?
##########################
Pycanon is a `Python`_ library which allows the user to know the anonymity level of a dataset based on a set of quasi-identifiers (QI), and a set of sensitive attributes. To do so, it provides a set of functions to compute the anonymity level of a dataset by means of the following techniques:

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

Install
***********************
We recommend using ``pip`` for installing *pycanon*:

.. code-block:: sh

    pip install pycanon
    
License
***********************
Pycanon is licensed under Apache License Version 2.0 (http://www.apache.org/licenses/)

Getting Started
***********************
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
