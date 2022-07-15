# pyCANON

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://gitlab.ifca.es/sainzj/check-anonymity/-/blob/main/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/pycanon/badge/?version=latest)](https://pycanon.readthedocs.io/en/latest/?badge=latest)

pyCANON is a library and CLI to assess the values of the paramenters associated
with the most common privacy-preserving techniques.

**Authors:** Judith Sáinz-Pardo Díaz and Álvaro López García (IFCA - CSIC).

## Installation

We recommend to use Python3 with [virtualenv](https://virtualenv.pypa.io/en/latest/):

    virtualenv .venv -p python3
    source .venv/bin/activate

Then run the following command to install the library and all its requirements:

    pip install py.canon

## Documentation

The pyCANON documentation is hosted on [Read the Docs](https://pycanon.readthedocs.io/).

## Getting started

Example using the [_adult dataset_](https://archive.ics.uci.edu/ml/datasets/adult):

- **Command line:**
    ```
    $ pycanon k-anonymity --qi age --qi education --qi occupation --qi relationship --qi sex --qi native-country adult.csv
    $ pycanon report --sa salary-class --qi age --qi education --qi occupation --qi relationship --qi sex --qi native-country adult.csv
    ```

- **Python API:**
    ```python
    from pycanon import anonymity, report

    FILE_NAME = "adult.csv"
    QI = ["age", "education", "occupation", "relationship", "sex", "native-country"]
    SA = ["salary-class"]

    # Calculate k for k-anonymity:
    k = anonymity.k_anonymity(FILE_NAME, QI)

    # Print the anonymity report:
    report.print_report(FILE_NAME, QI, SA)
    ```

## Description

pyCANON allows to check if the following privacy-preserving techniques are
verified and the value of the parameters associated with each of them:

| Technique                   | pyCANON function           | Parameters          | Notes                                                                                                                                                                                      |
|-----------------------------|----------------------------|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| k-anonymity                 | k_anonymity                | _k_: int            |                                                                                                                                                                                            |
| (α, k)-anonymity            | alpha_k_anonymity          | _α_: float _k_: int |                                                                                                                                                                                            |
| ℓ-diversity                 | l_diversity                | _ℓ_: int            | The function _achive_l_diversity_ can be used in order to obtain a new pandas dataframe where the records needed in order to get _ℓ-diversity_ for a given value of _ℓ_ have been removed. |
| Entropy ℓ-diversity         | entropy_l_diversity        | _ℓ_: int            |                                                                                                                                                                                            |
| Recursive (c,ℓ)-diversity   | recursive_c_l_diversity    | _c_: int _ℓ_: int   | Not calculated if ℓ=1. Note that, by definition: $` r_{1} < c(r_{l}+r_{l+1}+...+r_{m}) `$                                                                                                  |
| Basic β-likeness            | basic_beta_likeness       | _β_: float          |                                                                                                                                                                                            |
| Enhanced β-likeness         | enhanced_beta_likeness    | _β_: float          |                                                                                                                                                                                            |
| t-closeness                 | t_closeness      | _t_: float          | For numerical attributes the definition of the EMD (one-dimensional Earth Mover’s Distance) is used.  For categorical attributes, the metric "Equal Distance" is used.                     |
| δ-disclosure privacy | delta_disclosure | _δ_: float          |                                                                                                                                                                                            |
