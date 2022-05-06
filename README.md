# **check-anonymity**

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://gitlab.ifca.es/sainzj/check-anonymity/-/blob/main/LICENSE)

**Author:** Judith Sáinz-Pardo Díaz (IFCA - CSIC).

[[_TOC_]]

## Installation
We recommend to use Python3 with [virtualenv](https://virtualenv.pypa.io/en/latest/):
```
virtualenv venv -p python3
```
```
source venv/bin/activate
```
Then run the following command to install the library and all its requirements:
```
pip install git+https://gitlab.ifca.es/sainzj/check-anonymity
```

#### Use example:
Once the library is installed just import it as follows:
```python
from pycanon import test_anonymity
```
_Example:_ To find the value of _k_ for the k-anonymity condition of a file _data.csv_ with quisi-identifiers _QI_, execute:
```python
k = test_anonymity.calculate_k('data.csv', QI)
```

## Description 

Check if the following privacy-preserving techniques are verified and the value of the parameters associated with each of them:
- [x] _**k-anonymity:**_
    - _k_: int
- [x] _**(α, k)-anonymity:**_
    - _α_: float
    - _k_: int
- [x] _**l-diversity:**_
    - _l_: int
- [x] _**Entropy l-diversity:**_
    - _l_: int
- [x] _**Recursive (c,l)-diversity:**_
    - Not calculated if l=1. Note that, by definition: $` r_{1} < c(r_{l}+r_{l+1}+...+r_{m}) `$
    - _c_: int
    - _l_: int
- [x] _**Basic β-likeness:**_
    - _β_: float
- [x] _**Enhanced β-likeness:**_
    - _β_: float
- [x] _**t-closeness:**_:
    - For numerical attributes the definition of the EMD (one-dimensional Earth Mover’s Distance) is used.
    - For categorical attributes, the metric "Equal Distance" is used.
    - _t_: float
- [x] _**δ-disclosure privacy:**_
    - _δ_: float

**Note:** in this first version _k-map_ and _δ-presence_ are not studied because an auxiliar population table is needed. 

## Multiple sensitive attributes

In the case of multiple sensitve attributes, two approaches can be considered:
1. Calculate the different properties for each sensitive attribute individually, and take the maximum or minimum as appropriate (for example, the minumum value of _l_ for _l-diversity_ and the maximum value for _α_ in the case of _(α,k)-anonymity_).
2. Calculate the different properties for each sensitive attribute individually but modifying the set of quasi-identifiers by adding to this set, in addition to the initial quasi-identifiers, all the sensitive attributes except the one under analysis. Then, as in the previous approach, the minimum or maximum of each parameter as appropriate is taken. It is important to note that since the set of quasi-identifiers is updated each time the calculations are made for each SA, the computational cost is much higher in this case.

Specifically, in order to address this challenge, a parameter _gen_ is introduced in all functions except _k-anonymity_ (not applicable). If _gen=True_ (default value), the process of the first approach is followed: generalizing. Otherwise, the second approach is followed, updating the quasi-identifiers.


## Examples
1. Example using the [_adult dataset_](https://archive.ics.uci.edu/ml/datasets/adult). First, note that in de the folder _Data_ there are 3 files in which the dataset adult has been anonymized in different ways. Running _check_adult_anonymity.py_, we obtain the values of _k_ (for _k-anonymity_), _α_ (for _(α,k)-anonymity_), _l_ (for _l-diversity_), _l_ (for _entropy l-diversity_), _c_ (for _(c,l)-diversity_), _β_ (for _basic β-likeness_), _β_ (for _enhanced β-likeness_), _δ_ (for _δ-disclosure privacy_) and _t_ (for _t-closeness_) and associated to each of the 3 files, and a new file for each of them is saved, verifying now l-diversity with l=2.
2. Example using the [_drug type dataset_](https://www.kaggle.com/datasets/prathamtripathi/drug-classification), with the original data and with the data obtained after performing k-anonymization with k=5 with [ARX](https://arx.deidentifier.org/). Running _check_drug_data_anonymity.py_, we obtain the values of _k_ (for _k-anonymity_), _α_ (for _(α,k)-anonymity_), _l_ (for _l-diversity_), _l_ (for _entropy l-diversity_), _c_ (for _(c,l)-diversity_), _β_ (for _basic β-likeness_), _β_ (for _enhanced β-likeness_), _δ_ (for _δ-disclosure privacy_) and _t_ (for _t-closeness_) associated to each of the 2 datasets, and a new file for each of them is saved, verifying now l-diversity with l=2 (original data) and l=3 (anonymized data).
3. Example using the [_stroke prediction dataset_](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset) with the original data and with the data obtained after performing k-anonymization with k=2, 4, 10, 15, 19, 20, 22 and 25 with [ARX](https://arx.deidentifier.org/). Running _check_drug_data_anonymity.py_, we obtain the values of _k_ (for _k-anonymity_), _α_ (for _(α,k)-anonymity_), _l_ (for _l-diversity_), _l_ (for _entropy l-diversity_), _c_ (for _(c,l)-diversity_), _β_ (for _basic β-likeness_), _β_ (for _enhanced β-likeness_), _δ_ (for _δ-disclosure privacy_) and _t_ (for _t-closeness_) associated to each dataset, and a new file for each of them is saved, verifying now l-diversity with l=2.
4. Example using the [_student's math score dataset_](https://www.kaggle.com/datasets/soumyadiptadas/students-math-score-for-different-teaching-style), with the original data (after converting it from _.sav_ to _.csv_) and with the data obtained after performing k-anonymization with k=2, 5 and 7 with [ARX](https://arx.deidentifier.org/). Running _check_math_scores_data_anonymity.py_, we obtain the values of _k_ (for _k-anonymity_), _α_ (for _(α,k)-anonymity_), _l_ (for _l-diversity_), _l_ (for _entropy l-diversity_), _c_ (for _(c,l)-diversity_), _β_ (for _basic β-likeness_), _β_ (for _enhanced β-likeness_), _δ_ (for _δ-disclosure privacy_) and _t_ (for _t-closeness_) associated to each dataset, and a new file for each of them is saved, verifying now l-diversity for different _l_ values in each case.
5.  Example using the [_airline passenger satisfaction dataset_](https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction?select=test.csv), with the data obtained after performing k-anonymization with k=2, 5, 10 and 20 with [ARX](https://arx.deidentifier.org/). Running _check_airline_data_anonymity.py_, we obtain the values of _k_ (for _k-anonymity_), _α_ (for _(α,k)-anonymity_), _l_ (for _l-diversity_), _l_ (for _entropy l-diversity_), _c_ (for _(c,l)-diversity_), _β_ (for _basic β-likeness_), _β_ (for _enhanced β-likeness_), _δ_ (for _δ-disclosure privacy_) and _t_ (for _t-closeness_) associated to each dataset, and a new file for each of them is saved, verifying now l-diversity with l=2 (for all the sensitive attributes).

#### About the data
As mentioned in the previous section, different datasets are used for testing purposes, and the quasi-identifiers (QI) and sensitive attribute(s) (SA) are, in each case, the following:
- [_Adult dataset_](https://archive.ics.uci.edu/ml/datasets/adult): **QI** = ['age', 'education', 'occupation', 'relationship', 'sex', 'native-country'], **SA** = ['salary-class'].
- [_Drug type dataset_](https://www.kaggle.com/datasets/prathamtripathi/drug-classification): **QI** = ['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K'], **SA** = ['Drug'].
- [_Stroke prediction dataset_](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset): **QI** = ['gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'Residence_type', 'smoking_status'], **SA** = ['stroke'].
- [_Student's math score dataset_](https://www.kaggle.com/datasets/soumyadiptadas/students-math-score-for-different-teaching-style): **QI** = ['Teacher', 'Gender', 'Ethnic', 'Freeredu', 'wesson'], **SA** = ['Score'].
- [_Airline passenger satisfaction dataset_](https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction?select=test.csv): **QI** = ['Gender', 'Customer Type', 'Age', 'Type of Travel', 'Class', 'Flight Distance', 'Departure Delay in Minutes', 'Arrival Delay in Minutes'], **SA** = ['Departure/Arrival time convenient', 'Online boarding', 'On-board service', 'Inflight service', 'Cleanliness', 'satisfaction'].
